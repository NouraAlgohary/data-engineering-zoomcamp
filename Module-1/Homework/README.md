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

-------------
Question 5. Three biggest pickup zones

Which were the top pickup locations with over 13,000 in total_amount (across all trips) for 2019-10-18?

Consider only lpep_pickup_datetime when filtering by date.

```
SELECT puz."Zone", SUM("total_amount") AS max_total_amount
FROM green_taxi_data trips
JOIN zones puz
ON trips."PULocationID" = puz."LocationID"
WHERE DATE("lpep_pickup_datetime") = DATE '2019-10-18'
GROUP BY puz."Zone"
ORDER BY max_total_amount DESC;
```
<img width="611" alt="Screenshot 2025-01-30 at 10 56 36 PM" src="https://github.com/user-attachments/assets/2662649e-052e-43c9-9747-d77e080a4cbf" />


**Answer**
<img width="526" alt="Screenshot 2025-01-30 at 10 57 47 PM" src="https://github.com/user-attachments/assets/36c91bb4-4e15-4e1b-b9ae-3090be55fc30" />


-------------
Question 6. Largest tip

For the passengers picked up in October 2019 in the zone named "East Harlem North" which was the drop off zone that had the largest tip?

Note: it's tip , not trip

__Code__
```
SELECT doz."Zone", MAX(tip_amount) AS max_tip
FROM green_taxi_data trips
JOIN zones puz
ON trips."PULocationID" = puz."LocationID"
JOIN zones doz
ON trips."DOLocationID" = doz."LocationID"
WHERE puz."Zone" = 'East Harlem North'
GROUP BY doz."Zone"
ORDER BY max_tip DESC;
```
<img width="527" alt="Screenshot 2025-01-30 at 10 51 25 PM" src="https://github.com/user-attachments/assets/0eff5c25-a450-4224-8523-7f09f00ad729" />


**Answer**

<img width="215" alt="Screenshot 2025-01-30 at 10 52 28 PM" src="https://github.com/user-attachments/assets/81760f5d-d2bf-4cdb-9c28-ce58f659c865" />

