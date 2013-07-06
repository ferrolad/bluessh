
$(document).ready(function(){
	/* This code is executed after the DOM has been completely loaded */
        var Tabs;
	/* The available colors for the tabs: */
	var colors = ['blue','green','red','orange'];
	
	/* The colors of the line above the tab when it is active: */
	var topLineColor = {
		blue:'lightblue',
		green:'lightgreen',
		red:'red',
		orange:'orange'
	}
        /* Looping through the Tabs object: */
        var z=0;
        $.getJSON("/content/get_menu/",function(data){
            $.each(data,function(index,value){
                /* Sequentially creating the tabs and assigning a color from the array: */
                var tmp = $('<li><a href="'+value[1]+'" class="tab '+colors[(z++%4)]+'">'+value[0]+
                    ' <span class="left" /><span class="right" /></a></li>');
                /* Adding the tab to the UL container: */
                $('ul.tabContainer').append(tmp);
            });

            //划线函数
            function overLine(element){
                /* "this" points to the clicked tab hyperlink: */
                //var element = elem ? elem : $(this);

                /* Detecting the color of the tab (it was added to the class attribute in the loop above): */
                var bg = element.attr('class').replace('tab ','');

                /* Removing the line: */
                $('#overLine').remove();

                /* Creating a new line with jQuery 1.4 by passing a second parameter: */
                $('<div>',{
                    id:'overLine',
                    css:{
                        display:'none',
                    width:element.outerWidth()-2,
                    background:topLineColor[bg] || 'white'
                    }}).appendTo(element).fadeIn('fast');
            }

            var the_tabs = $('.tab');
            
            var cur_url=window.location.href.toLowerCase();
            
            //通过网址比对设置划线函数
            $("ul.tabContainer a").each(function(index){
                if(cur_url.indexOf($(this).attr("href").toLowerCase())>0)
                {
                    //alert($(this).attr("href"));
                    //alert(index);
                    overLine($(this));
                }
            });
        });//放到这里是为了防止ajax异步传输过程中元素未加载完成就被调用
});//end of $(document).ready(function(){

