import requests
import csv
import time

# 在这里填入你申请的高德API Key
api_key = "5cc693872916947b25dd4ff1afc67cf2"

def get_forklift_training_shops(city, keywords="叉车培训"):
    """
    获取指定城市的叉车培训店铺信息
    """
    url = "https://restapi.amap.com/v3/place/text"
    
    all_shops = []
    page = 1
    
    print(f"正在在 {city} 搜索 '{keywords}'...")
    
    try:
        while True:
            # 设置请求参数
            params = {
                'key': api_key,
                'keywords': keywords,
                'city': city,
                'offset': 20,  # 每页数量
                'page': page,
                'output': 'json',
                'extensions': 'all'
            }
            
            # 发送请求
            response = requests.get(url, params=params)
            data = response.json()
            
            # 检查请求是否成功
            if data['status'] == '1':
                shops = data['pois']
                if not shops:  # 如果没有数据了就停止
                    break
                
                for shop in shops:
                    shop_info = {
                        '名称': shop.get('name', ''),
                        '地址': shop.get('address', '暂无地址'),
                        '电话': shop.get('tel', '暂无电话') or '暂无电话',
                        '经纬度': shop.get('location', ''),
                        '城市': city
                    }
                    all_shops.append(shop_info)
                    print(f"找到: {shop_info['名称']} - 电话: {shop_info['电话']}")
                
                print(f"第 {page} 页完成，找到 {len(shops)} 条记录")
                page += 1
                time.sleep(0.2)  # 稍微延迟，避免请求太快
            else:
                print(f"请求失败: {data.get('info', '未知错误')}")
                break
                
    except Exception as e:
        print(f"出错: {e}")
    
    return all_shops

def save_to_file(shops, filename):
    """
    将数据保存到CSV文件
    """
    if not shops:
        print("没有找到数据，不保存文件")
        return
    
    with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=shops[0].keys())
        writer.writeheader()
        writer.writerows(shops)
    
    print(f"数据已保存到: {filename}")
    print(f"总共找到 {len(shops)} 家店铺")

# 主程序开始
if __name__ == "__main__":
    # 在这里设置你要搜索的城市
    target_city = "上海"  # 可以改成你想要的城市，如"上海"、"广州"等
    
    # 获取数据
    shops_data = get_forklift_training_shops(target_city)
    
    # 保存数据
    if shops_data:
        filename = f"{target_city}叉车培训店铺.csv"
        save_to_file(shops_data, filename)
        
        # 显示前几条结果
        print("\n=== 搜索结果预览 ===")
        for i, shop in enumerate(shops_data[:5], 1):  # 只显示前5条
            print(f"{i}. {shop['名称']}")
            print(f"   电话: {shop['电话']}")
            print(f"   地址: {shop['地址']}\n")
    else:
        print("没有找到相关店铺信息")