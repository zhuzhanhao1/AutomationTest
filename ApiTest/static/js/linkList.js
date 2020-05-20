layui.use(['form', 'layer', 'table'], function () {
    var table = layui.table;

    //友链列表
    var tableIns = table.render({
        elem: '#linkList',
        url: '/api/v1/link/list/',
        toolbar: '#toolbarDemo',

        page: {groups: 5}, //开启分页
        // cellMinWidth : 95,
        height: "full-104",
        limit: 10,
        limits: [10, 15, 20, 25],
        id: "linkListTab",
        size: 'lg',
        cols: [[
            {title: '操作', toolbar: '#barDemo', width: 60, align: "left"},
            {
                field: 'logo', title: 'LOGO', align: "center", templet: function (d) {
                    return '<a href="' + d.url + '" target="_blank"><img src="' + d.logo + '" height="26" /></a>';
                }
            },
            {field: 'websites', title: '网站名称'},

            {
                field: 'url', title: '网站地址', templet: function (d) {
                    return '<a class="layui-blue" href="' + d.url + '" target="_blank">' + d.url + '</a>';
                }
            }
        ]]
    });
    //监听行工具事件
    table.on('tool(linkList)', function (obj) {
        var data = obj.data;
        console.log(data);
        //编辑整个用例
        if (obj.event === 'update_link') {
            var update_link_layer = layer.open({
                type: 1,
                title: "编辑友链",
                area: ['35%', ""],
                skin: "layui-layer-molv",
                shada: 0.6,
                content: $("#update_link").html(),
                success: function () {
                    layui.use(['form', 'jquery'], function () {
                        var form = layui.form;
                        $ = layui.$;
                        var id = data.id;
                        form.val("update_link", {
                            "logo": data.logo,
                            "name": data.websites,
                            "url": data.url,
                        });
                        //监听编辑用户信息，
                        form.on('submit(update_link)', function (data) {
                            console.log(data.field);
                            $.ajax({
                                url: "/api/v1/link/update_link/" + String(id) + "/",
                                type: 'PUT',
                                data: {
                                    "logo": data.field.logo,
                                    "websites": data.field.name,
                                    "url": data.field.url
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
    });

})


//添加收藏
function add_link() {
    var add_link = layer.open({
        //layer提供了5种层类型。可传入的值有：0（信息框，默认）1（页面层）2（iframe层）3（加载层）4（tips层）
        type: 1,
        title: "添加收藏",
        area: ['40%', ''],
        shade: 0.6,
        skin: "layui-layer-rim",
        content: $("#add_link").html(),
        success: function () {
            layui.use(['form', 'jquery'], function () {
                var form = layui.form,
                    $ = layui.$;
                form.val("add_link");
                form.on('submit(add_link)', function (data) {
                    $.ajax({
                        url: "/api/v1/link/add_link/",
                        type: 'POST',
                        data: JSON.stringify({
                            "logo": data.field.logo,
                            "url": data.field.url,
                            "websites": data.field.name,
                        }),
                        headers: {
                            "Content-Type": "application/json"
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
