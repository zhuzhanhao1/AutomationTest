layui.use(['form','layer','table'],function(){
    var table = layui.table;

    //友链列表
    var tableIns = table.render({
        elem: '#linkList',
        url : '/api/v1/testurl/list/',
        //page : true,
        //cellMinWidth : 95,
        //height : "full-104",
        limit : 20,
        limits : [10,15,20,25],
        id : "linkListTab",
        size:'lg',
        cols : [[
            //{type: "checkbox", fixed:"left", width:50},
            {field: 'logo', title: 'LOGO',  align:"center",templet:function(d){
                return '<a href="'+d.url+'" target="_blank"><img src="'+d.logo+'" height="26" /></a>';
            }},
            {field: 'websites', title: '网站名称'},
            {field: 'url', title: '网站地址',templet:function(d){
                return '<a style="color:blue;" href="'+d.url+'" target="_blank">'+d.url+'</a>';
            }},
            {field: 'apidocument', title: '接口文档地址',templet:function(d){
                if (d.apidocument.indexOf("http") != -1){
                    return '<a style="color:blue;" href="'+d.apidocument+'" target="_blank">'+d.apidocument+'</a>';
                }else{
                    return '<span>'+d.apidocument+'</span>';
                }

            }}
        ]]
    });

})
