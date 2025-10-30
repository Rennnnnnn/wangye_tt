import requests
import csv
import time

# 在这里填入你申请的高德API Key
api_key = "5cc693872916947b25dd4ff1afc67cf2"

def get_forklift_training_shops(province, keywords="叉车培训"):
    """
    获取指定省份的叉车培训店铺信息
    """
    url = "https://restapi.amap.com/v3/place/text"
    
    all_shops = []
    page = 1
    
    print(f"正在在 {province} 搜索 '{keywords}'...")
    
    try:
        while True:
            # 设置请求参数 - 使用省份而不是城市
            params = {
                'key': api_key,
                'keywords': keywords,
                'city': province,  # 这里改为省份
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
                    # 构建完整的地址信息
                    pname = shop.get('pname', '')  # 省份
                    cityname = shop.get('cityname', '')  # 城市
                    adname = shop.get('adname', '')  # 区县
                    address = shop.get('address', '')  # 详细地址
                    
                    # 组合完整的地址
                    full_address = ""
                    if pname:
                        full_address += pname
                    if cityname and cityname != pname:  # 避免重复
                        full_address += cityname
                    if adname:
                        full_address += adname
                    if address:
                        full_address += address
                    
                    # 如果组合后为空，使用默认值
                    if not full_address:
                        full_address = "暂无详细地址"
                    
                    shop_info = {
                        '名称': shop.get('name', ''),
                        '省份': pname,
                        '城市': cityname,
                        '区县': adname,
                        '详细地址': address,
                        '完整地址': full_address,
                        '电话': shop.get('tel', '暂无电话') or '暂无电话',
                        '经纬度': shop.get('location', ''),
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
    # 在这里设置你要搜索的省份
    target_province = "浙江省"  # 搜索整个浙江省
    
    # 获取数据
    shops_data = get_forklift_training_shops(target_province)
    
    # 保存数据
    if shops_data:
        filename = f"{target_province}叉车培训店铺.csv"
        save_to_file(shops_data, filename)
        
        # 显示前几条结果
        print("\n=== 搜索结果预览 ===")
        for i, shop in enumerate(shops_data[:5], 1):  # 只显示前5条
            print(f"{i}. {shop['名称']}")
            print(f"   电话: {shop['电话']}")
            print(f"   完整地址: {shop['完整地址']}\n")
    else:
        print("没有找到相关店铺信息")