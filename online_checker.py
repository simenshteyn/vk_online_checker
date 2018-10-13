import vk

def check_online(public_id, app_token):
    token = app_token
    session = vk.Session()
    api = vk.API(session, v=5.80)
    result = []
    online = [0]

    def get_users_list(public_id, offset=0):
        count = offset
        users_list = api.groups.getMembers(access_token=token, group_id=str(public_id), offset=offset)
        if users_list['count'] <= 1000 or len(users_list['users']) < 1000:
            for i in range(len(users_list['users'])):
                result.append(users_list['users'][i])
            return
        elif (users_list['count'] % 1000 == 0
              and count == users_list['count'] - 1000):
            for i in range(len(users_list['users'])):
                result.append(users_list['users'][i])
            return
        else:
            for i in range(len(users_list['users'])):
                result.append(users_list['users'][i])
            count += 1000
            print('.')
            get_users_list(public_id, count)
        return result

    def get_online(list, count=0):
        """ Return count of online status from a given list of ids """
        if len(list) <= 1000:
            user_ids = str(list)[1:-1]
            users_list = api.users.get(access_token=token, user_ids=user_ids, fields='online')
            for user in users_list:
                count += user['online']
            online[0] = count
            return count
        else:
            user_ids = str(list[0:1000])[1:-1]
            users_list = api.users.get(access_token=token, user_ids=user_ids, fields='online')
            for user in users_list:
                count += user['online']
            get_online(list[1000:], count=count)
        return online[0]

    list = get_users_list(public_id)
    result = get_online(list)

    return 'Online: ' + str(result)

token = str(input('Enter your token: '))

while True:
    id = int(input('Enter public id: '))
    print(check_online(id, token))

