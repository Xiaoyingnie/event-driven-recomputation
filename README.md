# event-driven-recomputation

## Overview
In the event-driven system, messages are emitted onto an event bus. A worker service processes these events in real time, performing key calculations. However, an issue has occurred. Some events were missed or processed incorrectly due to an error. This solution demonstrates how to recalculate the results without relying on a traditional database for storing historical event data.

## Approach

### **1. How to recover and back-calculate the missing/incorrect data**
**Event Replay**:
   - Replay events from the event bus such as Kafka or event logs such as (AWS S3 / HDFS)
   - Reset the consumer offset to reprocess events from the point of failure
     
**Snapshoting**:
   - Periodically save snapshots of the system state to reduce the number of events that need to be replayed.
     
**Compensation Mechanism**:
   - For unrecoverable events, manually derive and correct the missing data based on the business logic.
     
**Idempotency**:
   - Ensure the worker service is idempotent, means that processing the same event multiple times does
    not cause side effects.
   - Use unique event identifiers to track the processed events.
### **2. Tools and Techniques**  
**Tools**:
- **Event Bus**: Kafka (event streaming and replay)
- **Storage**: AWS S3
- **Processing**: Apache Spark (if can tolerate micro-batch processing), Apace Flink (real-time event processing)
- **Scripting**: Python (for custome recalculation scripts)

**Techniques**:
- **Distributed Computing**: break down task into smaller sub-tasks and process them across multiple codes
- **Data Validation**: ensure the results are accurate and consistent with the business rules, including check the accuracy, consistency and completeness of the data.

### **3. How to ensure accuracy and consistency in the recalculated results**
- **Logging**: Log all recalculation steps and results for traebility and debugging.
- **Data Validation**: Compare the recalculated results with the known correct values and business rules.
- **Testing On Subset of Data**: Test the recalculation process with the subset od the data before applying it to the full data.
- **Concistency Checks**: Use checksums or hashes to verify the integrity of the recalculated data.

### **4. Solution**
- Python script ('recalculate_events.py') shows how to re-read events from a log and recalculate the results.

### **5. Summarize the approach**
**Event Replay**: Re-process eents from event bus (Kafka) or event logs (AWS S3 or HDFS) to recover missing or incorrect data.

**Idempotency**: Ensure the worker service can handle duplicate events without causing errors by using unique event identifiers ( event ID).

**Snapshotting**: Periodically save the system state snapshots to reduce the number of events that need to be replayed.

**Data Validation**: Validate the recalculated results against business rules to ensure accuracy and reasonability and consistency.

### **6. Why this approach**
**No dependency on traditionoal databases**: It uses event logs and distributed systems.

**Scalability**: Distributed computing allo system to handle high volumes of events efficiently.

**Flexibility**: Event replay and idempotency enable the system to recover from errors without manual intervention.

### **7. Trade-offs and Limitations**
**Trade-offs**: Replaying large number of events can be time-consuming and storing the event logs for replay requires large storage space.

**Limitations**:
- **Event Log Availability**: if event logs are lost, data recovery becomes impossible.
- **Real-time Constraintes**: replaying events and recalculating results would introduce latency.

### **8. If had access to more tools, how would approach change?**
**With access to a Database**:
- Store events and system state directly in the database
- query the database for the latest state instead of replaying events.
- Use database constraints to enforce data integrity.
  
**With access to eal-time stream processing framework (Apache Flink)**:
  - Use Flink's stateful processing and checkpointing features to simplify event replay and state recovery
  - leverage Flink's distributed processing capabilities to handle large volumes of events
    
### **If these tools applicable, how the solution scale to process millions of events per hour**
**Ingestion: Distributed Event Bus (Kafka)**:
- Kafka works as an event streaming ingestion system, enabling high-throughput and low-latency event ingestion.
- Partitioon events by key to distribute evenly
- Use multiple brokers to handle high volumes and ensure fault tolerance
- replicate partitions across brokers to ensure data durability
  
**Processing (Apache Flink)**:
  - Flink serves as a distributed stream processing framework, supporting fault-tolerance in a distributed way.
  - Flink processes events in parallel across the cluster of nodes.
  - Flink periodically saves snapshots of the state to storage (HDFS or S3) for fault tolerance.
  - Flink maintains state in memory, enabling efficient event processing

**Database for state management**:
- use ditributed database like cassandra, DynamoDB to handle high write and read throughput
- shard the database by key to ditribute the load
- batch writes to the database to reduce the number of transactions

**Event Log Storage**:
- store event logs in AWS S3 or HDFS, partition by date for efficient retrieval
- using incremental loading only save the changes data since last snapshot

**Data Validation**:
- use checksums or hashes to verify the integrity of the recalculated data, comapring it with a known correct hash
- use monitoring tools to track data quality and set up alerts for unexpected deviations

**Fault Tolerance**:
- Kafka replication ensures that no data loss i one broker fails
- use database replication to ensure high availability
- Flink checkpoint ensures fault tolerance by periodically save state to storage.

In summary, with Kafka, Flink and distributed database, the solution can handle millions of events per hour ensuring consistency, scalability and fault tolerance.





  
  

