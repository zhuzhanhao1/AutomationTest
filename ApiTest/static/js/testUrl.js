layui.use(['form','layer','table'],function(){
    var table = layui.table;

    //友链列表
    var tableIns = table.render({
        elem: '#linkList',
        url : '/api/v1/testurl/list/',
        toolbar: '#toolbarDemo',
        page : true,
        //cellMinWidth : 95,
        height: "full-104",
        limit : 10,
        limits : [10,15,20,25],
        id : "linkListTab",
        size:'lg',
        cols : [[
            {type: "checkbox"},
            {title: '操作', toolbar: '#barDemo', width: 100, align: "left"},
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
    table.on('tool(linkList)', function (obj) {
        var data = obj.data;
        console.log(data);
        //编辑整个用例
        if (obj.event === 'update_test_url') {
            var update_link_layer = layer.open({
                type: 1,
                title: "编辑友链",
                area: ['35%', ""],
                skin: "layui-layer-molv",
                shada: 0.6,
                content: $("#add_update_link").html(),
                success: function () {
                    layui.use(['form', 'jquery'], function () {
                        var form = layui.form;
                        $ = layui.$;
                        var id = data.id;
                        form.val("add_update_link", {
                            "logo": data.logo,
                            "websites": data.websites,
                            "url": data.url,
                            "apidocument":data.apidocument

                        });
                        //监听编辑用户信息，
                        form.on('submit(add_update_link)', function (data) {
                            console.log(data.field);
                            $.ajax({
                                url: "/api/v1/testurl/update_test_url/" + String(id) + "/",
                                type: 'PUT',
                                data: {
                                    "logo": data.field.logo,
                                    "websites": data.field.websites,
                                    "url": data.field.url,
                                    "apidocument":data.field.apidocument,
                                },
                                beforeSend: function () {
                                    l_index = layer.load(0, {shade: [0.5, '#DBDBDB']});
                                },
                                success: function (data) {
                                    if (data.code === 1000) {
                                        layer.msg(data.msg, {
                                            icon: 6, offset: "t"
                                        })
                                    } else {
                                        layer.msg(data.error, {
                                            icon: 5, offset: "t"
                                        })
                                    }
                                    $(".layui-laypage-btn").click();
                                },
                                error: function (data) {
                                    layer.msg("回调失败", {
                                        icon: 5,
                                        offset: 't',
                                        anim: 2,
                                    });
                                },
                                complete: function () {
                                    layer.close(l_index);
                                    layer.close(update_link_layer);
                                }

                            });
                            return false;//阻止表单跳转
                        });
                    });
                }
            });

        }
        else if (obj.event === 'del_test_url') {
            layer.confirm('真的删除行么', {icon: 2, title: "删除提示"}, function (index) {
                console.log(obj.data);
                //layer.msg("确定删除",{icon:1});
                obj.del();//删除对应行（tr）的DOM结构，并更新缓存
                layer.close(index);
                //向服务端发送删除指令
                var id = obj.data["id"];
                console.log(id);
                $.ajax({
                    url: "/api/v1/testurl/del_test_url/" + id + "/",
                    type: 'DELETE',
                    success: function (data) {
                        if (data.code === 1000) {
                            layer.msg(data.msg, {
                                icon: 6, offset: "t"
                            })
                        } else {
                            layer.msg(data.error, {
                                icon: 5, offset: "t"
                            })
                        }
                        $(".layui-laypage-btn").click();
                    },
                    error: function () {
                        layer.msg("回调失败", {
                            icon: 5,
                            offset: 't'
                        });
                    },
                });
            });
        }
    });

})

//添加收藏
function add_test_url() {
    var add_link = layer.open({
        //layer提供了5种层类型。可传入的值有：0（信息框，默认）1（页面层）2（iframe层）3（加载层）4（tips层）
        type: 1,
        title: "添加收藏",
        area: ['40%', ''],
        shade: 0.6,
        skin: "layui-layer-rim",
        content: $("#add_update_link").html(),
        success: function () {
            layui.use(['form', 'jquery'], function () {
                var form = layui.form,
                    $ = layui.$;
                form.val("add_update_link");
                form.on('submit(add_update_link)', function (data) {
                    $.ajax({
                        url: "/api/v1/testurl/add_test_url/",
                        type: 'POST',
                        data: {
                            "logo": data.field.logo,
                            "websites": data.field.websites,
                            "url": data.field.url,
                            "apidocument":data.field.apidocument,
                        },
                        success: function (data) {
                            if (data.code === 1000) {
                                layer.msg(data.msg, {
                                    icon: 6, offset: "t"
                                })
                            } else {
                                layer.msg(data.error, {
                                    icon: 5, offset: "t"
                                })
                            }
                            $(".layui-laypage-btn").click();
                        },
                        error: function () {
                            layer.msg("回调失败", {
                                icon: 5,
                                offset: 't'
                            });
                        },
                        complete: function () {
                            layer.close(add_link)

                        }
                    });
                    return false;//阻止表单跳转
                });


            });
        }
    });

}