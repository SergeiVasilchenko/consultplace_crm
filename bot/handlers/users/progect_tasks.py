# import logging
#
# import requests
# from aiogram import types
#
# from db_responce import log_get
# from filters import IsPrivate
# from .new_users.registration import FSMContext, RegState, account_text
# from keyboards.default import kb_start
# from keyboards.inline import kb_manage, ikb_acc_1_stage, ikb_acc_2_stage, ikb_acc_3_stage
# from loader import dp
#
#
# # TODO tasks from project
# @dp.message_handler(IsPrivate(), text='Мои проекты')
# async def acc_start(message: types.Message, state: FSMContext):
#     student_resp = log_get(url=f'http://194.67.86.225/ru/api/students/detail-update/{message.from_user.username}/')
#     student_id = student_resp['id'] if student_resp else 0
#     groups_resp = log_get(url=f'http://194.67.86.225/ru/api/students/groups/')
#     if groups_resp:
#         groups_id = [item['id'] for item in groups_resp if student_id in item['students']]
#         project_resp = log_get(url=f'http://194.67.86.225/ru/api/students/projects/')
#         if project_resp and groups_id:
#             for group_id in groups_id:
#                 projects_id = [item['id'] for item in groups_resp if group_id in item['group']]
#                 print(projects_id)
#
#
