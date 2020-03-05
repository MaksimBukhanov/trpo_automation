import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import email
import base64
import logging
import logging.config


logging.config.fileConfig('logging_config.conf')
logger = logging.getLogger(__name__)
service = get_service()
user_id = 'me'
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.labels']


def get_message(service, user_id):
	logger.info('Got into the get_message method')
	try:
		search_id = service.users().messages().list(userId=user_id, labelIds = ['INBOX']).execute()
		#список наших собщений в папке "Входящие"
		message_id = search_id['messages']
		logger.debug(f'message_id - {message_id}')
		#количество наших сообщений в папке
		number_results = search_id['resultSizeEstimate']
		logger.debug(f'number_results - {number_results}')

		while search_id['resultSizeEstimate'] > 0:
			alone_msg = message_id[0]
			id_of_msg = alone_msg['id']
			message_list = service.users().messages().get(userId=user_id, id=id_of_msg, format='full').execute()
			
			#Часть сообщения верхнего уровня с полезной информацией
			info_of_msg = message_list.get('payload')['headers']


			email_id = '' # Имя и ГуглМаил отправителя
			head_of_msg = '' # Тема письма
			body_of_msg = '' # Тело письма


			for head in info_of_msg :
				if head['name'] == 'From' :
					email_id = head['value']
				if head['name'] == 'Subject' :
					head_of_msg = head['value']
			body_of_msg = message_list['snippet']


			#if #метод Никиты отработал и нашел человека
				#отправляем письмо с фразами, что работа принята к рассмотрению
			#	if #метод Макса отработал и студент правильно запомнил 
					#сообщение
					##включаются остальные методы проверки работы
			#	else #если сообщение заполнено неверно, то высылается 
					#письмо отправителю о правильном заполнении писем

			#else #метод не нашел человека
				#отправляется письмо на авторизацию пользователя



			#архивация сообщения(403 недостаточно прав для gmail api с python)
			label_id = 'id_of_msg' 
			# ID of user label to add
			filter = {
				'criteria': {
					'from': 'email_id'
				},
				'action': {
					'addLabelIds': [label_id],
					'removeLabelIds': ['INBOX']
				}
				}
			result = service.users().settings().filters().create(userId=user_id, body=filter).execute()
			logger.info('Created filter: %s' % result.get('id'))			







	except (errors.HttpError. error):
		logger.exception(("An error occured: %s") % error)
	except Exception as ex:
		logger.exception(ex)
	finally:
		logger.info('The get_message method has completed its execution')
		return messages


def get_service():
	logger.info('Got into the get_service method')
	creds = None
	 # The file token.pickle stores the user's access and refresh tokens, and is
	 # created automatically when the authorization flow completes for the first
	 # time.
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service = build('gmail', 'v1', credentials=creds)
	print(service)
	logger.debug(f'service - {service}')
	logger.info('The get_service method has completed its execution')
	return service