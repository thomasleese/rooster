# Specification

## Architecture

- Web application consisting of a front-end for registering as a volunteer and a back-end for generating schedules and making changes.
- Python and Django, with MySQL as a database.
- The root object stored in the system is an event, which might be the "SR2016 Set-up", "SR2016 Competition" or "SR2016 Tear-down".
- Certain users are designated as schedule administrators per event.
- Events consist of a name, description, a duration and a number of time slots per day. It also consists of a number of jobs and a number of volunteers.
- All past events are stored in the system with an ability to "clone" an event for the next year.
- Jobs represent various roles which volunteers may be assigned to. They can specify to which time slots they are not applicable. A null job exists, which implies that a volunteer is free for that block of time.
- Resources are a way of representing the constraints in the system. For example, "People" are a resource which a volunteer provides (they are a "hidden" resource meaning they are not asked and they have a default value of one) and a job may require a number of "People" to be satisfied. Similarly, a resource might be "Years experience" where some of the more advanced jobs require a certain number of years experience. Jobs can express a minimum and target number of a resource.
- The schedule is generated internally and available as an HTML document, an iCal file, YAML file or an email sent automatically to volunteers. The schedule is also available per job and per volunteer.
- Jobs may also be manually assigned to volunteers per time slot and they will appear flagged up in the generated schedule.
- When registering as a volunteer, a list of jobs including their description and resources is presented and users may select a preference to be used as a fallback when generating the schedule.
- Provisional schedules may be generated at any point and not automatically sent out to volunteers.

## Built-in mandates

- Every volunteer can only do one job at a time.
- Every volunteer must do a null job at least once.
- At each interval, all jobs must be filled.
- Jobs cannot be assigned to unqualified volunteers.

## Initial Resource Ideas

- Willing to/already know the rules?	
- Knows about the competition software.
- Knows about the kit.
- Knows how to charge batteries.
- How many competitions have you volunteered at to?
- Willingness to speak to people?
- People	