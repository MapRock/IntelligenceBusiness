// Create nodes for each performance problem
CREATE 
(cpuPressure:Problem {name: 'CPU Pressure', description: 'Excessive CPU utilization by SQL Server causing slower response times.'}),
(memoryPressure:Problem {name: 'Memory Pressure', description: 'Insufficient available RAM for SQL Server processes causing performance degradation.'}),
(diskIO:Problem {name: 'Disk I/O Bottlenecks', description: 'Delays caused by disk subsystem not keeping up with the read/write request rate.'}),
(networkLatency:Problem {name: 'Network Latency', description: 'Issues with transmitting and receiving data packets quickly.'}),
(concurrencyIssues:Problem {name: 'Concurrency Issues', description: 'Problems arising from multiple queries contending for the same resource.'});

// Create nodes for metrics related to each problem
CREATE 
(processorTime:Metric {name: 'Processor Time %', description: 'Percentage of elapsed time the processor spends executing.'}),
(queryCompilations:Metric {name: 'SQL Compilations/s', description: 'Number of SQL compilations happening per second.'}),
(pageLife:Metric {name: 'Page Life Expectancy', description: 'Duration a data page is expected to stay in the buffer pool.'}),
(bufferHitRatio:Metric {name: 'Buffer Cache Hit Ratio %', description: 'Percentage of pages found in buffer without disk read.'}),
(pageReads:Metric {name: 'Page Reads/s', description: 'Rate at which pages are read from disk.'}),
(diskQueue:Metric {name: 'Disk Queue Length', description: 'Number of outstanding disk requests.'}),
(bytesReceived:Metric {name: 'Bytes Received/s', description: 'Rate of bytes received over the network.'}),
(lockWaits:Metric {name: 'Lock Waits/s', description: 'Number of locks per second that had to wait.'});
