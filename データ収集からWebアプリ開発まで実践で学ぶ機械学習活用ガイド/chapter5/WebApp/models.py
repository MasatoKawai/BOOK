import flaski.database
import flaski.dbmodels
import http.client, urllib.request, urllib.parse, urllib.error, base64
import requests
import json

# 予測確率のしきい値（パーセント）
threshold = 10

# モデルAPIの呼び出し
def callAPI(uploadFile):
	url = 'https://fishclassification0814-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/6404afa5-b2d7-4ca7-90f5-a4b6ec673a71/classify/iterations/Iteration1/image'
	headers={'content-type':'application/octet-stream','Prediction-Key':'57d09fdb5d32487f8b555a0e094e40f2'}
	#予測実行
	response =requests.post(url,data=open(uploadFile,"rb"), headers=headers)
	response.raise_for_status()
	analysis = response.json()
    
	result = []

	for prediction in range(len(analysis["predictions"])):
		if len(get_fish_data(analysis["predictions"][prediction]["tagName"])) != 0:
			# 確率がしきい値より大きいものを採用する
			if analysis["predictions"][prediction]["probability"] * 100 > threshold:
				result.append(get_fish_data(analysis["predictions"][prediction]["tagName"]))

	return result

# 魚情報をDBから取得し辞書型で返す
def get_fish_data(fishname):
	ses = flaski.database.db_session()
	fish_master = flaski.dbmodels.FishMaster
	fish_data = ses.query(fish_master).filter(fish_master.fish_name == fishname).first()

	fish_data_dict = {}
    
	if not fish_data is None:
		fish_data_dict['fish_name'] = fish_data.fish_name
		if fish_data.poison == 1:
			fish_data_dict['poison'] = '毒あり'
		else:
			fish_data_dict['poison'] = ''
		fish_data_dict['poison_part']     = fish_data.poison_part
		fish_data_dict['wiki_url']        = fish_data.wiki_url
		fish_data_dict['picture_path']    = fish_data.picture_path
		fish_data_dict['copyright_owner'] = fish_data.copyright_owner
		fish_data_dict['copyright_url']   = fish_data.copyright_url

	return fish_data_dict
