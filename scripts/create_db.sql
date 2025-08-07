-- Script to create database and user for FAPP
CREATE DATABASE fapp;
CREATE USER fappuser WITH ENCRYPTED PASSWORD 'fapp1234';
GRANT ALL PRIVILEGES ON DATABASE fapp TO fappuser;
