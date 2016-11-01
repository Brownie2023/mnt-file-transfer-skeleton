import datetime
import subprocess
import sys
import json
import os
import smtplib


def sendemail(to_addr_list, subject, message, from_addr='example_from@gmail.com', cc_addr_list=['example_cc@example.com'], login='example_from@gmail.com', password='ExamplePass', smtpserver='smtp.gmail.com:587'):
    header = 'From: %s\n' % from_addr
	header += 'To: %s\n' % ', '.join(to_addr_list)
	header += 'Cc: %s\n' % ', '.join(cc_addr_list)
	header += 'Subject: %s\n' % subject
	message = header + "\n\n" + message
	server = smtplib.SMTP(smtpserver)
	server.starttls()
	server.login(login, password)
	problems = server.sendmail(from_addr, to_addr_list, message)
	server.quit()

def mount(srvr_one, srvr_two):
    FNULL = open(os.devnull, 'w')
	try:
		subprocess.check_call(srvr_one, shell=True, stdout=FNULL, stderr=FNULL)
		subprocess.check_call(srvr_two, shell=True, stdout=FNULL, stderr=FNULL)
	except subprocess.CalledProcessError: 
		print "Unable to mount"
		msg = "Unable to mount drives for file transfer."
		sendemail(to_addr_list=["example_to@example.com"], subject="Mount Failed", message=msg)
		unmount(hbtis_string, storage_string)


def unmount(srvr_one, srvr_two):
	FNULL = open(os.devnull, 'w')
	try:
		subprocess.call(srvr_one, shell=True, stdout=FNULL, stderr=FNULL)
		subprocess.call(srvr_two, shell=True, stdout=FNULL, stderr=FNULL)
	except subprocess.CalledProcessError:
		print "Unable to unmount"
		msg = "Unable to unmount drives after file transfer."
		sendemail(to_addr_list=["eaxample_to@example.com"], subject="Unmount Failed", message=msg)
		sys.exit(1)

def copyFile(filename, extension, date, copy, local_one, local_two, value):
	FNULL = open(os.devnull, 'w')
	copy_string = copy + " " + local_one + filename + extension + " " + local_two + filename + extension
	copy_rename_string = copy + " " + local_one + filename + extension + " " + local_two + filename + "_" + date + extension
	try:
		subprocess.call(copy_string, shell=True, stdout=FNULL, stderr=FNULL)
		subprocess.call(copy_rename_string, shell=True, stdout=FNULL, stderr=FNULL)
		if value == "true":
			msg = "Transferred REVISED: " + filename + " to mount"
		else:
			msg = "Transferred: " + filename + " to mount"
		sendemail(to_addr_list=["example_to@example.com"], subject=filename + " transfer", message=msg)
	except subprocess.CalledProcessError: 
		print "Unable to copy" + filename + " to mount"
		if value == "true":
			msg = "Unable to transfer REVISED: " + filename
		else:
			msg = "Unable to transfer: " + filename
		sendemail(to_addr_list=["example_to@example.com"], subject=filename + " transfer failed", message=msg)

if __name__ == '__main__':
	#Must pass in json string: '{"":""}'
	json_string = sys.argv[1]
	back_office_dict = json.loads(json_string)
	current_date = datetime.datetime.now().strftime("%Y%m%d_%H%M")
	#Mount Variables
	local_mnt_one = "/mnt/server_mount1/"
	local_mnt_two = "/mnt/server_mount2/"
	srvr_one_mnt_str = "mount -t cifs -o username=<domain>/<username>,password=<password> //<server>/SMB/share/dir " + local_mnt_one
	srvr_two_mnt_str = "mount -t cifs -o username=<domain>/<username>,password=<password> //<server>/SMB/share/dir " + local_mnt_two
	srvr_one_umnt_string = "umount " + local_mnt_one
	srvr_two_umnt_string = "umount " + local_mnt_two
	#Report Variables
	crew_filename = "Crew_Schedule" #pdf
	weekly_schedule_filename = "Weekly_Schedule" #pdf
	pdf_extension = ".pdf"
	copy_command = "/bin/cp"
	copied_list = []

	mount(srvr_one_mnt_str, srvr_two_mnt_str)

	for key, value in back_office_dict.iteritems():
		if value is not None:
			if key == "Crew":
				copied_list.append(crew_filename)
				copyFile(crew_filename, pdf_extension, current_date, copy_command, local_mnt_one, local_mnt_two, value)
			elif key == "WeeklySchedule":
				copied_list.append(weekly_schedule_filename)
				copyFile(weekly_schedule_filename, pdf_extension, current_date, copy_command, local_mnt_one, local_mnt_two, value)

			print "copied files: " + ', '.join(map(str, copied_list))

	unmount(srvr_one_umnt_string, srvr_two_umnt_string)

	server.quit()

	sys.stdout.flush()
