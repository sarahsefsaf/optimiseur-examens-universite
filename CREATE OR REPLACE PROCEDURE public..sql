CREATE OR REPLACE PROCEDURE public.assign_all_professors()
 LANGUAGE plpgsql
AS $procedure$
DECLARE
    exam RECORD;
BEGIN
    -- Clean previous assignments
    DELETE FROM surveillances;

    -- Assign professors exam by exam
    FOR exam IN
        SELECT id FROM examens ORDER BY date_exam, heure_debut
    LOOP
        CALL assign_professors_to_exam(exam.id);
    END LOOP;

    RAISE NOTICE '✅ Professors assigned to all exams';
END;
$procedure$;

CREATE OR REPLACE PROCEDURE public.assign_exam_dates_by_cohort(IN start_date date DEFAULT '2026-01-06'::date, IN max_days integer DEFAULT 35)
 LANGUAGE plpgsql
AS $procedure$
DECLARE
    cohort RECORD;
    exam RECORD;
    current_day DATE;
    day_index INT;
    exams_today INT;
BEGIN
    -- Reset dates
    UPDATE examens SET date_exam = NULL;

    -- Loop over each cohort (department + level)
    FOR cohort IN
        SELECT DISTINCT m.departement_id, e.niveau
        FROM examens e
        JOIN modules m ON m.id = e.module_id
        ORDER BY m.departement_id, e.niveau
    LOOP
        day_index := 0;

        -- Schedule exams of THIS cohort
        FOR exam IN
            SELECT e.id
            FROM examens e
            JOIN modules m ON m.id = e.module_id
            WHERE m.departement_id = cohort.departement_id
              AND e.niveau = cohort.niveau
            ORDER BY e.id
        LOOP
            LOOP
                current_day := start_date + day_index;

                IF day_index >= max_days THEN
                    RAISE EXCEPTION
                        '❌ Cannot schedule exams for department %, level % within % days',
                        cohort.departement_id, cohort.niveau, max_days;
                END IF;

                -- Global limit: max 9 exams per day
                SELECT COUNT(*) INTO exams_today
                FROM examens
                WHERE date_exam = current_day;

                -- Cohort rule
                IF exams_today < 9
                   AND NOT EXISTS (
                        SELECT 1
                        FROM examens e2
                        JOIN modules m2 ON m2.id = e2.module_id
                        WHERE e2.date_exam = current_day
                          AND e2.niveau = cohort.niveau
                          AND m2.departement_id = cohort.departement_id
                   )
                THEN
                    UPDATE examens
                    SET date_exam = current_day
                    WHERE id = exam.id;

                    EXIT;
                END IF;

                day_index := day_index + 1;
            END LOOP;
        END LOOP;
    END LOOP;

    RAISE NOTICE '✅ Exam dates assigned correctly over % days', max_days;
END;
$procedure$;

CREATE OR REPLACE PROCEDURE public.assign_exam_times()
 LANGUAGE plpgsql
AS $procedure$
DECLARE
    exam RECORD;
    slot_index INT := 0;

    time_slots TIME[] := ARRAY[
        TIME '08:30',
        TIME '10:19',
        TIME '12:08',
        TIME '13:57',
        TIME '15:46'
    ];
BEGIN
    -- Reset times
    UPDATE examens SET heure_debut = NULL;

    FOR exam IN
        SELECT id
        FROM examens
        WHERE date_exam IS NOT NULL
        ORDER BY date_exam, id
    LOOP
        UPDATE examens
        SET heure_debut = time_slots[(slot_index % array_length(time_slots, 1)) + 1]
        WHERE id = exam.id;

        slot_index := slot_index + 1;
    END LOOP;

    RAISE NOTICE '✅ Exam times assigned using fixed slots';
END;
$procedure$;

CREATE OR REPLACE PROCEDURE public.assign_professors_to_exam(IN p_exam_id integer)
 LANGUAGE plpgsql
AS $procedure$
DECLARE
    exam_dept INT;
    prof RECORD;
    assigned INT := 0;
BEGIN
    -- Get exam department
    SELECT m.departement_id
    INTO exam_dept
    FROM examens e
    JOIN modules m ON m.id = e.module_id
    WHERE e.id = p_exam_id;

    --------------------------------------------------
    -- 1️⃣ Same department first
    --------------------------------------------------
    FOR prof IN
        SELECT p.id
        FROM professeurs p
        WHERE p.departement_id = exam_dept
        ORDER BY RANDOM()
    LOOP
        EXIT WHEN assigned >= 4;

        IF can_prof_supervise_exam(prof.id, p_exam_id)
        AND NOT EXISTS (
            SELECT 1 FROM surveillances
            WHERE professeur_id = prof.id
              AND examen_id = p_exam_id
        ) THEN
            INSERT INTO surveillances(professeur_id, examen_id)
            VALUES (prof.id, p_exam_id);
            assigned := assigned + 1;
        END IF;
    END LOOP;

    --------------------------------------------------
    -- 2️⃣ Other departments if needed
    --------------------------------------------------
    IF assigned < 3 THEN
        FOR prof IN
            SELECT p.id
            FROM professeurs p
            WHERE p.departement_id <> exam_dept
            ORDER BY RANDOM()
        LOOP
            EXIT WHEN assigned >= 3;

            IF can_prof_supervise_exam(prof.id, p_exam_id)
            AND NOT EXISTS (
                SELECT 1 FROM surveillances
                WHERE professeur_id = prof.id
                  AND examen_id = p_exam_id
            ) THEN
                INSERT INTO surveillances(professeur_id, examen_id)
                VALUES (prof.id, p_exam_id);
                assigned := assigned + 1;
            END IF;
        END LOOP;
    END IF;

    --------------------------------------------------
    -- 3️⃣ Log conflict
    --------------------------------------------------
    IF assigned < 3 THEN
        INSERT INTO exam_conflicts(exam_id, conflict_type, conflict_detail)
        VALUES (
            p_exam_id,
            'Not enough professors',
            'Only ' || assigned || ' professors assigned'
        );
    END IF;
END;
$procedure$;

CREATE OR REPLACE PROCEDURE public.assign_profs_by_department(IN p_exam_id integer)
 LANGUAGE plpgsql
AS $procedure$
DECLARE
    prof RECORD;
    dept_id INT;
    assigned_count INT := 0;
    can_assign BOOLEAN;
    min_profs INT := 3;
    max_profs INT := 4;
BEGIN
    -- Get department of the exam
    SELECT m.departement_id
    INTO dept_id
    FROM examens e
    JOIN modules m ON e.module_id = m.id
    WHERE e.id = p_exam_id;

    -- Assign professors from same department first
    FOR prof IN
        SELECT * FROM professeurs
        WHERE departement_id = dept_id
        ORDER BY RANDOM()
    LOOP
        -- Check max 3 exams per day and no same-time conflict
        can_assign := check_prof_exam_per_day(prof.id, p_exam_id);
        IF can_assign THEN
            INSERT INTO surveillances(professeur_id, examen_id)
            VALUES (prof.id, p_exam_id);
            assigned_count := assigned_count + 1;
        END IF;

        EXIT WHEN assigned_count >= max_profs;
    END LOOP;

    -- If not enough professors, assign from other departments
    IF assigned_count < min_profs THEN
        FOR prof IN
            SELECT * FROM professeurs
            WHERE departement_id <> dept_id
            ORDER BY RANDOM()
        LOOP
            can_assign := check_prof_exam_per_day(prof.id, p_exam_id);
            IF can_assign THEN
                INSERT INTO surveillances(professeur_id, examen_id)
                VALUES (prof.id, p_exam_id);
                assigned_count := assigned_count + 1;
            END IF;

            EXIT WHEN assigned_count >= min_profs;
        END LOOP;
    END IF;

    IF assigned_count < min_profs THEN
        INSERT INTO exam_conflicts(exam_id, conflict_type, conflict_detail)
        VALUES(p_exam_id, 'Not enough professors', 'Assigned ' || assigned_count || ' professors, needed at least ' || min_profs);
    END IF;

END;
$procedure$;


CREATE OR REPLACE PROCEDURE public.assign_rooms_and_students_time_safe()
 LANGUAGE plpgsql
AS $procedure$
DECLARE
    exam_rec RECORD;
    student_rec RECORD;

    room_id INT;
    room_capacity CONSTANT INT := 20;
    room_index INT;
BEGIN
    -- Clean previous assignments
    DELETE FROM exam_room_students;

    ------------------------------------------------------------------
    -- Loop through exams
    ------------------------------------------------------------------
    FOR exam_rec IN
        SELECT id
        FROM examens
        WHERE date_exam IS NOT NULL
    LOOP
        -- Ensure exam has rooms
        IF NOT EXISTS (
            SELECT 1
            FROM exam_salle_affectation
            WHERE exam_id = exam_rec.id
        ) THEN
            RAISE EXCEPTION '❌ Exam % has no rooms assigned', exam_rec.id;
        END IF;

        room_index := 0;

        ------------------------------------------------------------------
        -- Loop through students
        ------------------------------------------------------------------
        FOR student_rec IN
            SELECT i.etudiant_id
            FROM inscriptions i
            WHERE i.examen_id = exam_rec.id
            ORDER BY i.etudiant_id
        LOOP
            -- Pick room
            SELECT salle_id
            INTO room_id
            FROM exam_salle_affectation
            WHERE exam_id = exam_rec.id
            ORDER BY salle_id
            OFFSET room_index
            LIMIT 1;

            IF room_id IS NULL THEN
                RAISE EXCEPTION
                    '❌ Not enough rooms for exam % (need more rooms)',
                    exam_rec.id;
            END IF;

            INSERT INTO exam_room_students (exam_id, salle_id, etudiant_id)
            VALUES (exam_rec.id, room_id, student_rec.etudiant_id);

            -- Move to next room after 20 students
            IF (
                SELECT COUNT(*)
                FROM exam_room_students
                WHERE exam_id = exam_rec.id
                  AND salle_id = room_id
            ) >= room_capacity THEN
                room_index := room_index + 1;
            END IF;
        END LOOP;
    END LOOP;

    RAISE NOTICE '✅ Rooms and students assigned correctly (max 20 per room)';
END;
$procedure$;

CREATE OR REPLACE PROCEDURE public.assign_rooms_to_exams()
 LANGUAGE plpgsql
AS $procedure$
DECLARE
    exam RECORD;
    room RECORD;
    students_count INT;
    rooms_needed INT;
    rooms_assigned INT;
BEGIN
    -- Clean previous room assignments
    DELETE FROM exam_salle_affectation;
    UPDATE examens SET salle_id = NULL;

    FOR exam IN
        SELECT id, date_exam, heure_debut
        FROM examens
        WHERE date_exam IS NOT NULL
          AND heure_debut IS NOT NULL
        ORDER BY date_exam, heure_debut, id
    LOOP
        -- Number of students for this exam
        SELECT COUNT(*) INTO students_count
        FROM inscriptions
        WHERE examen_id = exam.id;

        rooms_needed := CEIL(students_count / 20.0);
        rooms_assigned := 0;

        FOR room IN
            SELECT s.id
            FROM salles s
            WHERE NOT EXISTS (
                SELECT 1
                FROM exam_salle_affectation esa
                JOIN examens e2 ON e2.id = esa.exam_id
                WHERE esa.salle_id = s.id
                  AND e2.date_exam = exam.date_exam
                  AND e2.heure_debut = exam.heure_debut
            )
            ORDER BY s.id
        LOOP
            INSERT INTO exam_salle_affectation(exam_id, salle_id)
            VALUES (exam.id, room.id);

            rooms_assigned := rooms_assigned + 1;
            EXIT WHEN rooms_assigned >= rooms_needed;
        END LOOP;

        IF rooms_assigned < rooms_needed THEN
            INSERT INTO exam_conflicts(exam_id, conflict_type, conflict_detail)
            VALUES (
                exam.id,
                'Not enough rooms',
                CONCAT('Needed ', rooms_needed, ', assigned ', rooms_assigned)
            );
        END IF;
    END LOOP;

    RAISE NOTICE '✅ Rooms assigned to exams';
END;
$procedure$;

CREATE OR REPLACE PROCEDURE public.reset_exam_time_and_rooms()
 LANGUAGE plpgsql
AS $procedure$
BEGIN
    -- Clear dependent assignments first
    DELETE FROM exam_room_students;
    DELETE FROM exam_salle_affectation;
    DELETE FROM surveillances;

    -- Reset exam scheduling fields
    UPDATE examens
    SET
        date_exam   = NULL,
        heure_debut = NULL;

    -- Clear conflicts (they are now obsolete)
    DELETE FROM exam_conflicts;

    RAISE NOTICE '✅ Exam time, rooms, surveillances, and conflicts have been reset';
END;
$procedure$;

CREATE OR REPLACE PROCEDURE public.schedule_all_professors()
 LANGUAGE plpgsql
AS $procedure$
DECLARE
    exam_rec RECORD;
BEGIN
    -- Loop through all exams
    FOR exam_rec IN SELECT id FROM examens LOOP
        -- Assign professors for each exam
        PERFORM assign_profs_by_department(exam_rec.id);
    END LOOP;

    RAISE NOTICE '✅ All professors assigned to exams!';
END;
$procedure$;

CREATE OR REPLACE PROCEDURE public.schedule_all_students()
 LANGUAGE plpgsql
AS $procedure$
BEGIN
    -- 1️⃣ Reset everything first
    CALL reset_exam_time_and_rooms();

    -- 2️⃣ Assign exam dates per cohort (department + level)
    CALL assign_exam_dates_by_cohort('2026-01-06', 35);

    -- 3️⃣ Assign exam times
    CALL assign_exam_times();

    -- 4️⃣ Assign rooms and split students safely
    CALL assign_rooms_and_students_time_safe();

    RAISE NOTICE '✅ All student exams scheduled successfully!';
END;
$procedure$;


CREATE OR REPLACE FUNCTION public.can_prof_supervise_exam(p_prof_id integer, p_exam_id integer)
 RETURNS boolean
 LANGUAGE plpgsql
AS $function$
DECLARE
    exam_date DATE;
    exam_time TIME;
    exams_count INT;
BEGIN
    -- Get exam date & time
    SELECT date_exam, heure_debut
    INTO exam_date, exam_time
    FROM examens
    WHERE id = p_exam_id;

    -- 1️⃣ Same-time conflict
    IF EXISTS (
        SELECT 1
        FROM surveillances s
        JOIN examens e ON e.id = s.examen_id
        WHERE s.professeur_id = p_prof_id
          AND e.date_exam = exam_date
          AND e.heure_debut = exam_time
    ) THEN
        RETURN FALSE;
    END IF;

    -- 2️⃣ Max 3 exams per day
    SELECT COUNT(*) INTO exams_count
    FROM surveillances s
    JOIN examens e ON e.id = s.examen_id
    WHERE s.professeur_id = p_prof_id
      AND e.date_exam = exam_date;

    IF exams_count >= 3 THEN
        RETURN FALSE;
    END IF;

    RETURN TRUE;
END;
$function$;
