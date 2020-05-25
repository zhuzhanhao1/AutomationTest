layui.use(['tree', "table"], function () {
    var tree = layui.tree
        , layer = layui.layer;
    var table = layui.table;
    $.ajax({
        url: "/api/v1/menu/tree/",
        type: 'GET',
        success: function (data) {
            tree.render({
                elem: '#test'
                , data: data
                //,showCheckbox: true  //是否显示复选框
                , edit: ['add', 'update', 'del'] //操作节点的图标
                , id: 'demoId1'
                , isJump: true //是否允许点击节点时弹出新窗口跳转
                //, onlyIconControl: true  //是否仅允许节点左侧图标控制展开收缩
                , click: function (obj) {
                    var data = obj.data;  //获取当前点击的节点数据
                    console.log(data);
                    layer.msg('状态：' + obj.state + '<br>节点数据：' + JSON.stringify(data.title));
                    var title = data.title;
                    var tableIns = table.render({
                        elem: '#treetable',
                        url: '/api/v1/menu/table/',
                        toolbar: '#toolbarDemo',
                        page: {groups: 5}, //开启分页
                        // cellMinWidth : 95,
                        height: "full-104",
                        limit: 10,
                        limits: [10, 15, 20, 25],
                        id: "linkListTab",
                        size: 'lg',
                        where: {
                            "title": data.title
                        },
                        cols: [[
                            {type: 'checkbox'},
                            {title: '操作', toolbar: '#barDemo', width: 100, align: "left"},
                            {field: 'title', title: '标题值'},
                            {field: 'nav', title: '标题键'},
                            {
                                field: 'icon', title: '图标', templet: function (d) {
                                    console.log(d.icon);
                                    return '<span>' + d.icon + '</span>';
                                }
                            },
                            {field: 'href', title: '链接'},
                            {field: 'spread', title: '是否展开'},
                        ]]
                    });
                    table.on('tool(treetable)', function (obj) {
                        //编辑整个用例
                        if (obj.event === 'update_childmenu') {
                            var data = obj.data;
                            console.log(data);
                            var update_childmenu = layer.open({
                                //layer提供了5种层类型。可传入的值有：0（信息框，默认）1（页面层）2（iframe层）3（加载层）4（tips层）
                                type: 1,
                                title: "编辑字菜单",
                                area: ['40%', ''],
                                shade: 0.6,
                                skin: "layui-layer-rim",
                                content: $("#add_childmenu").html(),
                                success: function () {
                                    layui.use(['form', 'jquery'], function () {
                                        var form = layui.form,
                                            $ = layui.$;
                                        form.val("add_childmenu", {
                                            "title": data.title,
                                            "icon": data.icon,
                                            "href": data.href,
                                            "nav": data.nav,
                                            "spread": data.spread//开关状态
                                        });
                                        var onoff = "";
                                        form.on('switch(switchTest)', function (data) {
                                            console.log(data.othis);
                                            onoff = this.checked ? 'true' : 'false';
                                            layer.msg('开关checked：' + (this.checked ? 'true' : 'false'), {
                                                offset: '6px'
                                            });
                                            console.log(onoff);
                                            //layer.tips('温馨提示：请注意开关状态的文字可以随意定义，而不仅仅是ON|OFF', data.othis)
                                        });
                                        let tabledata = data;
                                        form.on('submit(add_childmenu)', function (data) {
                                            if (onoff == "") {
                                                onoff = "false"
                                            }
                                            $.ajax({
                                                url: "/api/v1/menu/update_childmenu/" + tabledata.id + "/",
                                                type: 'PUT',
                                                data: {
                                                    "area": tabledata.area,
                                                    "classification": tabledata.classification,
                                                    "title": data.field.title,
                                                    "icon": data.field.icon,
                                                    "href": data.field.href,
                                                    "spread": onoff,//开关状态
                                                    "nav": data.field.nav,
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
                                                    layer.close(update_childmenu)

                                                }
                                            });
                                            return false;//阻止表单跳转
                                        });


                                    });
                                }
                            });

                        } else if (obj.event === 'del_childmenu') {
                            layer.confirm('真的删除行么', {icon: 2, title: "删除提示"}, function (index) {
                                console.log(obj.data);
                                //layer.msg("确定删除",{icon:1});
                                obj.del();//删除对应行（tr）的DOM结构，并更新缓存
                                layer.close(index);
                                //向服务端发送删除指令
                                var id = obj.data["id"];
                                console.log(id);
                                $.ajax({
                                    url: "/api/v1/menu/del_childmenu/" + id + "/",
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
                    table.on('toolbar(treetable)', function (obj) {
                        var checkStatus = table.checkStatus(obj.config.id);
                        switch (obj.event) {
                            case 'add_childmenu':
                                var res = checkStatus.data;
                                console.log(res.length);
                                var add_childmenu = layer.open({
                                    //layer提供了5种层类型。可传入的值有：0（信息框，默认）1（页面层）2（iframe层）3（加载层）4（tips层）
                                    type: 1,
                                    title: "添加字菜单",
                                    area: ['40%', ''],
                                    shade: 0.6,
                                    skin: "layui-layer-rim",
                                    content: $("#add_childmenu").html(),
                                    success: function () {
                                        layui.use(['form', 'jquery'], function () {
                                            var form = layui.form,
                                                $ = layui.$;
                                            form.val("add_childmenu");
                                            var onoff = "";
                                            form.on('switch(switchTest)', function (data) {
                                                console.log(data.othis);
                                                onoff = this.checked ? 'true' : 'false';
                                                //layer.msg('开关checked：' + (this.checked ? 'true' : 'false'), {offset: '6px'});
                                                console.log(onoff);
                                                //layer.tips('温馨提示：请注意开关状态的文字可以随意定义，而不仅仅是ON|OFF', data.othis)
                                            });
                                            form.on('submit(add_childmenu)', function (data) {
                                                if (onoff == "") {
                                                    onoff = "false"
                                                }
                                                console.log(title);
                                                $.ajax({
                                                    url: "/api/v1/menu/add_childmenu/",
                                                    type: 'POST',
                                                    data: {
                                                        "classification": title,
                                                        "title": data.field.title,
                                                        "icon": data.field.icon,
                                                        "href": data.field.href,
                                                        "spread": onoff,//开关状态,
                                                        "nav": data.field["nav"],
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
                                                        layer.close(add_childmenu)

                                                    }
                                                });
                                                return false;//阻止表单跳转
                                            });


                                        });
                                    }
                                });


                        }
                    });
                }
            });
        },
        error: function () {
            layer.msg("回调失败", {
                icon: 5,
                offset: 't'
            });
        },
    });
});
