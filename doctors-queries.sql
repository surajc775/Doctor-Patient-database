#What are the first names and last names of the patients who have cardiologists for primary care providers (PCP)?

select a.first_name, a.last_name 
from patient a, doctor b 
where b.specialty = 'Cardiology' and a.doctor_id = b.doctor_id;


#What are the first names and last names of the patients who saw their doctor (PCP) in May 2010?

select a.first_name, a.last_name
from patient a, visit b
where date_format(b.visit_date, '%m/%Y') = '05/2010' 
and a.patient_id = b.patient_id;


#OPTIONAL BONUS (5 points): What are the first name and last name of the doctor who has the most patients (not the most visits)?

select first_name, last_name
from doctor
where doctor_id = (select doctor_id from 
(select doctor_id, count(*)
from patient
group by doctor_id
order by 2 desc
LIMIT 1) x);
