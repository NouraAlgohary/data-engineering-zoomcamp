project <br/>
├── Dockerfile<br/>
├── docker-compose.yml<br/>
├── ingestion_script.py<br/>

Question 3. Trip Segmentation Count

During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, respectively, happened:

Up to 1 mile
In between 1 (exclusive) and 3 miles (inclusive),
In between 3 (exclusive) and 7 miles (inclusive),
In between 7 (exclusive) and 10 miles (inclusive),
Over 10 miles
```
SELECT 
	COUNT(CASE WHEN trip_distance <= 1 THEN 1 END) AS "Up to 1 mile",
	COUNT(CASE WHEN trip_distance > 1 AND trip_distance <= 3 THEN 1 END) AS "In between 1 and 3 miles",
	COUNT(CASE WHEN trip_distance > 3 AND trip_distance <= 7 THEN 1 END) AS "In between 3 and 7 miles",
	COUNT(CASE WHEN trip_distance > 7 AND trip_distance <= 10 THEN 1 END) AS "In between 7 and 10 miles",
	COUNT(CASE WHEN trip_distance > 10 THEN 1 END) AS "Over 10 miles"
FROM green_taxi_data
WHERE DATE(lpep_pickup_datetime) >= DATE '2019-10-01'
AND DATE(lpep_pickup_datetime) < DATE '2019-11-01';
```
<img width="1015" alt="Screenshot 2025-01-30 at 10 38 11 PM" src="https://github.com/user-attachments/assets/aa00e9f3-00ec-478b-9368-b44ce431cbab" />

**Answer**
<img width="607" alt="Screenshot 2025-01-30 at 10 42 41 PM" src="https://github.com/user-attachments/assets/a7321837-5b4e-4d6c-a7a0-3bd400bca086" />


Question 4. Longest trip for each day

Which was the pick up day with the longest trip distance? Use the pick up time for your calculations.
```
SELECT DATE(lpep_pickup_datetime), MAX(trip_distance) max_trip_distance
FROM green_taxi_data
GROUP BY DATE(lpep_pickup_datetime)
ORDER BY max_trip_distance DESC

```
<img width="1015" alt="Screenshot 2025-01-30 at 10 42 02 PM" src="https://github.com/user-attachments/assets/ad44e6ac-a7b3-4c01-bd49-52937350ec8d" />

**Answer**
<img width="305" alt="Screenshot 2025-01-30 at 10 42 58 PM" src="https://github.com/user-attachments/assets/ba0f8517-c613-43c1-a240-b9b7f46eb398" />





