SET GLOBAL time_zone = 'America/Chicago';

USE enceladus;

CREATE TABLE denials (
	denialid int NOT NULL AUTO_INCREMENT,
    groupname varchar(64) NOT NULL,
	filedate Date NOT NULL,
	grandtotal float(8,2) NOT NULL default 0.0,
	filename varchar(32) NOT NULL,
	PRIMARY KEY (denialid)
);

CREATE TABLE adjustments (
	adjustmentid int NOT NULL AUTO_INCREMENT,
    denialid int NOT NULL,
    claimid varchar(16) NOT NULL,
    keytype varchar(3) NOT NULL,
    amount float(8,2) NOT NULL default 0.0,
	PRIMARY KEY (adjustmentid),
    FOREIGN KEY (denialid) REFERENCES denials(denialid)
);


















