SELECT 
  SUM(`i`.`sale_dollars`) AS `sale_dollars`, 
  SUM(`i`.`bottles_sold`) AS `bottles_sold`, 
  `i`.`Store` AS `Store`,
  `i`.`Year` AS `Year`
FROM 
  `Eugene Training`.`iowa_liquor_sales` `i`  
WHERE 
  `i`.`Zip Code` = '50613' 
 GROUP BY `i`.`Store`, `i`.`Year`
