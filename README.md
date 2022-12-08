# isedol_twitch_alert_bot
이세돌 관련 텔레그램 알림봇 제작한 것들을 모아두었습니다  

## on-offline_alert
이세돌 멤버분들과 우왁굳님의 방송이 온ㅡ오프 될 때마다 알림을 보내줍니다  

## chat_alert
이세돌 멤버들과 우왁굳님의 채팅을 바로 수집해서 알림을 보내줍니다  
채팅 수집은 이세돌 멤버, 우왁굳님, 뢴트게늄님, 천양님 채팅창에서만 수집합니다

## title_alert
이세돌 멤버분들의 방송 제목이 변경될 때마다 알림을 보내줍니다  

## connect
트위치 API 인증, 텔레그램 연결 class가 있습니다  

## example_response
requests.get('https://api.twitch.tv/helix/channels?broadcaster_id=' + isedol_bc_id[mem_num], headers=headers)  
의 내용 예시를 적어두었습니다