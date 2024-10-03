from module1 import mysql

cur = mysql.connection.cursor()


def create_stored_procedures(cur):
    procedures = [
        """
       CREATE DEFINER=`root`@`localhost` PROCEDURE `add_product`(IN id int,
        IN name varchar(20),
        IN description varchar(100),
        IN price int,
        IN category varchar(100),
        IN image varchar(100),
        IN qty int
        )
        BEGIN
          insert into products(id,name,description,price,category,image,qty) values(id,name,description,price,category,image,qty);
        END
        """,
        """
              CREATE DEFINER=`root`@`localhost` PROCEDURE `add_to_cart`(IN userId INT, IN productId INT, IN qty1 INT, IN price INT)
        BEGIN
            DECLARE existing_qty INT;
            
            -- Check if the item is already in the cart
            SELECT quantity INTO existing_qty
            FROM cart
            WHERE user_id = userId AND product_id = productId;
            
            IF existing_qty IS NOT NULL THEN
                -- Update the quantity if the item is already in the cart
                UPDATE cart
                SET quantity = quantity + qty1
                WHERE user_id = userId AND product_id = productId;
            ELSE
                -- Insert a new record if the item is not in the cart
                INSERT INTO cart (user_id, product_id, quantity, price_at_time)
                VALUES (userId, productId, qty1, price);
            END IF;
            UPDATE ecommerce.products SET qty = qty - qty1 where id = productId;
        END
        """
        ,
        """
         CREATE DEFINER=`root`@`localhost` PROCEDURE `add_user_data`(IN name varchar(20),
           IN email varchar(30),
           IN password varchar(10),
           IN mobile varchar(12)
           )
        BEGIN
          insert into users (name,email,password,phone) values(name,email,password,mobile);
        END
        """,
        """
         CREATE DEFINER=`root`@`localhost` PROCEDURE `addProduct`(IN cid int, IN q int)
        BEGIN
            DECLARE pid int;
            DECLARE current_qty int;
           
               -- Get the current product id and quantity
               SELECT product_id, quantity INTO pid, current_qty FROM cart WHERE id = cid;
               
                    -- Update the cart and products tables
               UPDATE cart SET quantity = quantity + q WHERE id = cid;
               UPDATE products SET qty = qty - q WHERE id = pid;
        END
        """,

        """
        CREATE DEFINER=`root`@`localhost` PROCEDURE `buy_products`(IN uid int)
        BEGIN
          SELECT name,quantity,(quantity*price_at_time) as Total_Price from ecommerce.cart JOIN ecommerce.products where cart.product_id=products.id and user_id=uid;
        END
        """,
        """
          CREATE DEFINER=`root`@`localhost` PROCEDURE `cart_products`(IN uid int)
            BEGIN
              select  ecommerce.products.name,ecommerce.products.description, ecommerce.cart.quantity,  ecommerce.products.price*ecommerce.cart.quantity as TotalPrice, ecommerce.cart.product_id, ecommerce.cart.id from ecommerce.products JOIN ecommerce.cart ON ecommerce.products.id = ecommerce.cart.product_id where ecommerce.cart.user_id=uid;
            END
        """
        ,

        """
         CREATE DEFINER=`root`@`localhost` PROCEDURE `fetch_product`()
        BEGIN
          select * from products;
        END
        """
        ,
        """
        CREATE DEFINER=`root`@`localhost` PROCEDURE `new_password`(IN new_password varchar(20), IN email varchar(45))
        BEGIN
          update ecommerce.users set password=new_password where ecommerce.users.email=email; 
        END
                
        """,
        """
        CREATE DEFINER=`root`@`localhost` PROCEDURE `updateCart`(IN cid int, IN q int)
        BEGIN
           DECLARE pid int;
           DECLARE current_qty int;
           
           -- Get the current product id and quantity
           SELECT product_id, quantity INTO pid, current_qty FROM cart WHERE id = cid;
           
           -- Ensure the cart quantity doesn't go negative
           IF current_qty < q THEN
              SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Quantity in cart cannot be less than zero';
           END IF;
           
           -- Update the cart and products tables
           UPDATE cart SET quantity = quantity - q WHERE id = cid;
           UPDATE products SET qty = qty + q WHERE id = pid;
        END
        """
    ]

    for procedure in procedures:
        try:
            cur.execute(procedure)
        except Exception as e:
            print(f"Error creating procedure: {e}")
            raise
