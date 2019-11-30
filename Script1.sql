create table customer(
custID varchar(10) not null primary key,
CustName char(50) not null,
Email varchar(100) not null
);

create table frequentCust(
custID varchar(10) not null,
AccountNumber numeric(15) not null,
CCNumber numeric(16) not null,
ExpiryDate date not null,
foreign key (custID) references customer
);

create table infrequentCust(
custID varchar(10) not null,
CCNumber numeric(16) not null,
ExpiryDate date not null,
foreign key (custID) references customer
);

create table products(
productID varchar(10) not null,
productType char(15)
);

alter table products
add primary key (productID);

alter table products
add price numeric(12,8);

/*------relation-------*/
create table orders(
custID varchar(10) not null,
productID varchar(10) not null,
foreign key (custID) references customer,
foreign key (productID) references products
);

create table address_table(
addrID varchar(10) primary key,
addressLine1 varchar(20) not null,
addressLine2 varchar(20),
zipcode numeric(6) not null,
city char(15) not null,
state_a char(2) not null
);

create table stores(
storeID varchar(10) not null primary key,
addrID varchar(10) not null,
foreign key (addrID) references address_table
);

/*------relation------*/
create table contains_prod(
storeID varchar(10) not null,
productID varchar(10) not null,
foreign key (storeID) references stores,
foreign key (productID) references products
);

create table warehouse(
warehouseID varchar(10) primary key,
storeID varchar(10) not null,
addrID varchar(10) not null,
foreign key (addrID) references address_table,
foreign key (storeID) references stores
);

alter table warehouse
add quantity numeric(3);

/*-------relation-----*/
create table stocks(
warehouseID varchar(10),
productID varchar(10),
foreign key (warehouseID) references warehouse,
foreign key (productID) references products
);

/*------relation------*/
create table sends(
warehouseID varchar(10) not null,
storeID varchar(10) not null,
foreign key (warehouseID) references warehouse,
foreign key (storeID) references stores
);

create table supplier(
supplierID varchar(10) primary key
);

create table company(
companyName char(20) primary key
);
/*-------relation-----*/
create table gets(
supplierID varchar(10) not null,
productID varchar(10) not null,
foreign key (supplierID) references supplier,
foreign key (productID) references products
);
/*-------relation-----*/
create table produces(
companyName char(20) not null,
productID varchar(10) not null,
foreign key (companyName) references company,
foreign key (productID) references products
);
/*-------relation-----*/
create table supplies(
warehouseID varchar(10),
supplierID varchar(10),
foreign key (warehouseID) references warehouse,
foreign key (supplierID) references supplier
);
/*-------relation-----*/
create table sc(
supplierID varchar(10),
companyName char(20),
foreign key (supplierID) references supplier,
foreign key (companyName) references company
);

create table transactions(
transactionID varchar(10) primary key,
custID varchar(10),
addrID varchar(10),
foreign key (custID) references customer,
foreign key (addrID) references address_table
);

create table orders_prod(
orderID varchar(10) primary key,
orderDate date,
orderTime timestamp,
orderQty numeric(10,3),
transactionID varchar(10),
foreign key (transactionID) references transactions
);
/*-------relation-----*/
create table located_at(
addrID varchar(10),
storeID varchar(10),
warehouseID varchar(10),
foreign key (addrID) references address_table,
foreign key (storeID) references stores,
foreign key (warehouseID) references warehouse
);
/*-------relation-----*/
create table online_order(
warehouseID varchar(10),
orderID varchar(10),
foreign key (warehouseID) references warehouse,
foreign key (orderID) references orders_prod
);

create table shipper(
trackingID varchar(20),
shipperName char(20),
primary key (trackingID,shipperName)
);
/*-------relation-----*/
create table takes(
orderID varchar(10),
trackingID varchar(20),
shipperName char(20),
foreign key (orderID) references orders_prod,
foreign key (trackingID,shipperName) references shipper
);
/*-------relation-----*/
create table delivers(
addrID varchar(10),
trackingID varchar(20),
shipperName char(20),
foreign key (addrID) references address_table,
foreign key (trackingID,shipperName) references shipper
);

create table laptop_spec(
lapName varchar(10) not null primary key,
productID varchar(10) not null,
companyName char(20) not null,
screenresolution varchar(10),
processor varchar(10),
RAM varchar(20),
GPU varchar(20),
internalStorage varchar(20),
lapOS varchar(10),
lapOS_version varchar(10),
foreign key(productID) references products,
foreign key(companyName) references company
);

create table phone_spec(
phoneName varchar(20) not null primary key,
productID varchar(10) not null,
companyName char(20) not null,
phoneStorage varchar(20),
color char(10),
frontcampixel varchar(10),
backcampixel varchar(10),
processor varchar(10),
extStoragecapacity varchar(10),
phoneOS varchar(10),
phoneOS_version varchar(10),
foreign key(productID) references products,
foreign key(companyName) references company
);

create table tablet_spec(
tabName varchar(20) not null primary key,
productID varchar(10) not null,
companyName char(20) not null,
screenResolution varchar(10),
processor varchar(10),
RAM varchar(20),
tabStorage varchar(10),
tabOS varchar(10),
tabOS_version varchar(10),
foreign key(productID) references products,
foreign key(companyName) references company
);

create sequence cust_seq
  minvalue 1
  maxvalue 999999999999999999999999999
  start with 1
  increment by 1
  cache 20;

create or replace trigger cust_seq_trig
before update on customer
for each row 
begin
  :NEW.custID := cust_seq.NEXTVAL;
end;

create sequence ord_seq
  minvalue 1
  maxvalue 999999999999999999999999999
  start with 1
  increment by 1
  cache 20;
  
create or replace trigger ord_seq_trig
after update on transactions
for each row 
begin
   update orders_prod set 
   orderID = ord_seq.NEXTVAL;
end;

create table phoneandspec
(
  productID varchar(10),
  phoneName varchar(20),
  foreign key (productID) references products,
  foreign key (phoneName) references phone_spec
);

create or replace view show_by_product as
select 
case 
when productType='Phone' then a where a in (select * from phone_spec)
when productType='Laptop' then b where b in  (select * from laptop_spec)
else c where c in (select * from tablet_spec)
end
from products;

create view show_by_product_phone
as
  select *
  from phone_spec s join phoneandspec p on s.productID=p.productID;