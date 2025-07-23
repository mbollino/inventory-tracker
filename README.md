## Inventory Tracker
[Zoja Inventory Tracker]()

## Logo:
![alt text](main_app/static/images/main-logo.png)

## Description of Inventory Tracker App:
My application is designed for any company to track their inventory.  For the purposes of the assignment, I created a Women's Fashion Boutique to use the app. I focused on keeping the design simple and easy to use. They can add all their inventory, track orders, add suppliers.  My user authentication was created for group authentication, so they can assign and admin for their group and then assign duties for each group, so some employees may only view information while others can update.

## Attributions
[CatCollector](https://generalassembly.instructure.com/courses/630/pages/django-crud-app-cat-collector)

## Technologies Used
Python  
Django  
PostgreSQL
HTML  
CSS  

## Stretch Goals
Add update function to Orders with separate Order display page  
Update Order - options will include 'Canceled', 'Lost', 'Damaged', 'Received'  
If Received, included date received - when click "add" or "udpate", automatic add to quantity  
When Order updated, it is moved to Past Orders and out of Current Order List; Link to Past Orders is included on Product Detail page in the Orders box; If clicked, past orders list will display.  Can click on any order to see details of order.  
Add Products Sold update to Inventory - will update daily - will have automatic fill in date when updated - will also automatically deduct inventory from quantity when updated  
Add option to add additional contact info to Supplier, such as a second person or customer service general contact  
Add field to each product - 'min quantity required to carry' and change conditional logic to highlight when the inventory level falls at or below that number for each product  
Ultimately, if this were a real app, I would want to be able to create a cash register/checkout system for it so that will update the inventory as products are sold  
Also make sure it can be modified for a distributor/wholesaler so they can track orders on a larger scale  
