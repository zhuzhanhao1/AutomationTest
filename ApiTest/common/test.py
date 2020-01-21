import jsonpath

dic_name = [{"id": "2ef834f6-24f2-4434-93f0-ef799f78f24b", "objectName": "KJ.科技档案", "code": "KJ", "name": "科技档案", "parentId": None,
  "fileSchemeId": "ea1a5bbd-4f26-4d2f-be8c-b1ebf7994e74", "volumeSchemeId": "e697d28f-215e-440c-bded-6bd5d38a898b",
  "top": True, "bottom": False, "collectionWay": "record"},
 {"id": "d6814dee-1ccb-48ed-94d4-5b530300fbf0", "objectName": "WS.文书档案", "code": "WS", "name": "文书档案", "parentId": None,
  "fileSchemeId": None, "volumeSchemeId": None, "top": True, "bottom": False, "collectionWay": "volume"}]

shop={
    "store": {
        "book": [
            {
                "category": "reference",
                "author": "Nigel Rees",
                "title": "Sayings of the Century",
                "price": 8.95
            },
            {
                "category": "fiction",
                "author": "Evelyn Waugh",
                "title": "Sword of Honour",
                "price": 12.99
            },
            {
                "category": "fiction",
                "author": "Herman Melville",
                "title": "Moby Dick",
                "isbn": "0-553-21311-3",
                "price": 8.99
            },
            {
                "category": "fiction",
                "author": "J. R. R. Tolkien",
                "title": "The Lord of the Rings",
                "isbn": "0-395-19395-8",
                "price": 22.99
            }
        ],
        "bicycle": {
            "color": "red",
            "price": 19.95
        }
    },
    "expensive": 10
}
# res=jsonpath.jsonpath(dic_name,'$..[?(@.code=="WS")].id')
# print(res)
# res=jsonpath.jsonpath(dic_name,'$..id')
# print(res)
# book_lg10=jsonpath.jsonpath(shop,'$..book[?(@.isbn)].price.[1]')
# print(book_lg10)
acl = {
	"description": "访问控制策略名称",
	"displayName": "访问控制策略描述信息",
	"accessorName": [
		"replace1"],
	"permitValue": [
	6]
}
res=jsonpath.jsonpath(acl,'$.accessorName.[0]')
print(res)

dependkey_a = {"$..id":0}
dependkey_ab = [x for x in dependkey_a]
print(dependkey_ab)
