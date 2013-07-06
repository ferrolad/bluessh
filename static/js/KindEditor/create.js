var editor;
KindEditor.ready(function(K) {
    editor = K.create('#id_content', {
        resizeMode : 2,
        height : 400,
        allowFileManager : true,
        uploadJson : 'http://forsave.sinaapp.com/ke_upload_json', // 相对于当前页面的路径
    });
});
