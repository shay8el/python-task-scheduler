insert into occurrences(title, details) values
("User Created", "some details"),
("User Logged In", "some other details");

insert into occurrences(title, details,due_time) values
("John's birthday party", "at john's House","2019-10-23 16:00:00"),
("Important meeting", "meet with George and Steve","2019-10-23 16:00:00"),
("Rick and Morty season 4 release", "at David's House","2019-10-23 16:00:00"),
("Maccabi Tel-Aviv vs. Hapoel Beer-Sheva", "at Bloomfield stadium","2019-10-23 16:00:00");

insert into actions(name, location, args) values
("notification", "executor/example_actions/send_notification.py", "{'default_arg':'aaa'}"),
("email", "executor/example_actions/send_email.py", "{'service_token':'cba321'}"),
("sms", "executor/example_actions/send_sms.py", "{'service_token':'abc123'}");
