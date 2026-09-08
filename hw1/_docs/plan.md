# NYC Restaurant Explorer

## Overview

NYC Restaurant Explorer is a small web application that helps a group of friends discover restaurants in New York City and keep track of places they want to try together.

The application will use restaurant data from an external NYC dataset or API. Users will not need accounts. Instead, each person will type their name when using the application and can flag or unflag restaurants they are interested in visiting.

The main goal is to make it easy to identify restaurants that multiple friends want to visit.

## Target Users

The application is intended for small groups of friends who are deciding where to eat in New York City.

Users should be able to use the app without creating an account or logging in.

## Core Features

### 1. Browse NYC Restaurants

Users can browse restaurants sourced from an external NYC restaurant dataset or API.

Each restaurant should display basic information such as:

* Restaurant name
* Borough
* Cuisine
* Address

### 2. Search and Filter Restaurants

Users can narrow down the restaurant list using:

* Restaurant name search
* Borough filter
* Cuisine filter

Filters should make it easier to find relevant restaurants without having to browse the entire dataset.

### 3. Want to Go

A user types their name before interacting with restaurant flags.

For each restaurant, the user can toggle a **Want to Go** flag.

If the user has not flagged the restaurant, clicking Want to Go adds their interest.

If the user has already flagged the restaurant, clicking it again removes their interest.

The application should prevent the same person from creating duplicate flags for the same restaurant.

### 4. Shared Matches

Each restaurant should display the names of friends who have flagged it.

When two or more people have flagged the same restaurant, the application should visually highlight that restaurant as a shared match.

This allows the group to quickly identify restaurants that multiple people want to visit.

## Data

Restaurant information will come from an external NYC dataset or API.

The first version will use restaurant information primarily for discovery rather than analysis.

The application should store user-created Want to Go flags locally in the application's database.

A flag should connect:

* A person's entered name
* A restaurant
* Their Want to Go status

## User Flow

1. A user opens the application.
2. The user types their name.
3. The user browses or searches the NYC restaurant list.
4. The user can filter restaurants by borough or cuisine.
5. The user clicks Want to Go on restaurants they are interested in.
6. The application records their interest.
7. The user can click the same control again to remove their interest.
8. Restaurants show which friends want to visit them.
9. Restaurants with two or more interested friends are highlighted as shared matches.

## Out of Scope for Version 1

The first version will not include:

* User accounts or passwords
* Reservations
* Restaurant reviews
* Ratings written by users
* Social networking features
* Messaging between friends
* Maps or route planning
* Recommendation algorithms
* Restaurant owners adding or editing listings

## Success Criteria

The first version is successful if a group of friends can:

* Browse real NYC restaurant data
* Search and filter restaurants
* Identify themselves by typing a name
* Flag and unflag restaurants
* See who else wants to visit each restaurant
* Easily identify restaurants that have interest from at least two people
