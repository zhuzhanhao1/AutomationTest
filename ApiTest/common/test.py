import jsonpath

dic_name = [{"id": "2ef834f6-24f2-4434-93f0-ef799f78f24b", "objectName": "KJ.科技档案", "code": "KJ", "name": "科技档案", "parentId": None,
  "fileSchemeId": "ea1a5bbd-4f26-4d2f-be8c-b1ebf7994e74", "volumeSchemeId": "e697d28f-215e-440c-bded-6bd5d38a898b",
  "top": True, "bottom": False, "collectionWay": "record"},
 {"id": "4a3b0d39-5df1-4521-bf6d-8d7eb07ccaf8", "objectName": "ZP.照片档案", "code": "ZP", "name": "照片档案", "parentId": None,
  "fileSchemeId": "81a4fb38-71e1-4d26-8e8b-b9b044c94cb7", "volumeSchemeId": "", "top": True, "bottom": False,
  "collectionWay": "record"},
 {"id": "4b3d1335-03eb-4aad-829a-cfe86d60e9ca", "objectName": "YJ.移交表单测试", "code": "YJ", "name": "移交表单测试",
  "parentId": None, "fileSchemeId": "4773410f-4aef-4bbf-a9a0-10f1f0e9389d", "volumeSchemeId": None, "top": True,
  "bottom": True, "collectionWay": "record"},
 {"id": "4d0a986e-5d48-4db5-8cda-73b65aff9ee3", "objectName": "A.朱占豪测试", "code": "A", "name": "朱占豪测试", "parentId": None,
  "fileSchemeId": None, "volumeSchemeId": None, "top": True, "bottom": False, "collectionWay": "record"},
 {"id": "67210905-bee9-4ad1-8764-0691c51300e7", "objectName": "LY.录音档案", "code": "LY", "name": "录音档案", "parentId": None,
  "fileSchemeId": "0cd2008a-0ebc-4775-ace8-7ec318313d38", "volumeSchemeId": None, "top": True, "bottom": True,
  "collectionWay": "record"},
 {"id": "9e815722-4517-43be-8774-031bfe0b9f46", "objectName": "ZY.专业档案", "code": "ZY", "name": "专业档案", "parentId": None,
  "fileSchemeId": None, "volumeSchemeId": None, "top": True, "bottom": False, "collectionWay": "record"},
 {"id": "a3ba8b9f-9b29-4c70-b29c-f2e7640d9783", "objectName": "ZJCS.组件测试", "code": "ZJCS", "name": "组件测试",
  "parentId": None, "fileSchemeId": "bf7b10c9-d479-4287-9c15-8b8e377e18c6", "volumeSchemeId": None, "top": True,
  "bottom": True, "collectionWay": "record"},
 {"id": "bcd8b1c3-7924-4f95-b2f3-9b095e97c21d", "objectName": "XZ.行政事项", "code": "XZ", "name": "行政事项", "parentId": None,
  "fileSchemeId": "b8a55516-8033-4d9e-97f1-7303bf14f8e4", "volumeSchemeId": None, "top": True, "bottom": True,
  "collectionWay": "record"},
 {"id": "c8b6ee92-2165-4003-be9a-c136860bf5b3", "objectName": "DZZL.电子资料", "code": "DZZL", "name": "电子资料",
  "parentId": None, "fileSchemeId": "f045c1fa-1d2e-4b15-b6b0-02291d0b0d65", "volumeSchemeId": None, "top": True,
  "bottom": True, "collectionWay": "record"},
 {"id": "d6814dee-1ccb-48ed-94d4-5b530300fbf0", "objectName": "WS.文书档案", "code": "WS", "name": "文书档案", "parentId": None,
  "fileSchemeId": None, "volumeSchemeId": None, "top": True, "bottom": False, "collectionWay": "volume"},
 {"id": "f16c5c4f-2753-4c79-8215-d5dae23a5c0c", "objectName": "CX.测试", "code": "CX", "name": "测试", "parentId": None,
  "fileSchemeId": "fb757763-ff7b-4c18-97ed-bf4914e58663", "volumeSchemeId": None, "top": True, "bottom": True,
  "collectionWay": "record"},
 {"id": "f1cd6497-9ce6-4783-bd70-3bae367f1ee3", "objectName": "LX.录像档案", "code": "LX", "name": "录像档案", "parentId": None,
  "fileSchemeId": "", "volumeSchemeId": "", "top": True, "bottom": False, "collectionWay": ""}]

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
res=jsonpath.jsonpath(dic_name,'$..id')
print(res)
# book_lg10=jsonpath.jsonpath(shop,'$..book[?(@.isbn)].price.[1]')
# print(book_lg10)