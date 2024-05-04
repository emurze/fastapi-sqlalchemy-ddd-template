# Transaction Problems

### Read is safe operation (no lock)

### Update

* Lost Update Problem
  * Just update is safely because of MVCC (multi version concurrency control) and deadlock + performance
  * if you have select then use For Update
  * Isolation level

* Unrepeatable Read Problem
  * use For Update
  * Isolation level

* Phantom String Problem
  * use For Update
  * Isolation level

### Delete

* Cascade Deletes using DeleteEvents

* Ubi Dahan (just don't delete)

### Insert

* Try to combine aggregate roots

* ...



### Anomalies

* Dirty Strings - READ COMMITTED
* Lost Update - for update
* Unrepeatable Read - for update
* Phantom String - for update
