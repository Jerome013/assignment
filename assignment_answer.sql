With orderSale as (SELECT a.*, b.*, c.*,d.* 
						FROM orders a
							INNER JOIN sales b ON a.sales_id = b.sales_id
							INNER JOIN items c ON a.item_id = c.item_id
							INNER JOIN customers d ON b.customer_id = d.customer_id
								WHERE d.age BETWEEN 18 and 35
								)
								
SELECT
		customer_id AS customer,
		age,
		item_name AS item,
		sum(quantity)
FROM orderSale
WHERE quantity IS NOT NULL
	GROUP BY
		item, customer
	ORDER BY
		customer;
		
		
				
				
		
				