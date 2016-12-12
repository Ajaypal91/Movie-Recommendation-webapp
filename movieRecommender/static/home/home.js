function loadPage() {
    NProgress.start();
    loadData()

}


function loadData()
 {
    $userNameDiv = $('.welcomeHeader')[0];
    username = $userNameDiv.textContent.replace(" Welcome ","")
    userID = $userNameDiv.id;
    //show the header div
    $('.welcomeHeader').addClass('fadeInAnimation').show()
         $.getJSON('/getHomePageData', {
        name: username,
        userid:userID,
        },
        function(response){
            if (response.status == -1) {
                updateHTMLForNoHistory(response.data);
                showLeftTab();
                $('.logout').removeClass("hide").addClass('show');
                NProgress.done();
            }
            else if (response.status) {
                updateHTML(response.data);
                showTabs();
                $('.logout').removeClass("hide").addClass('show');
                NProgress.done();
            }
            else {
                $('#errorDiv').show();
                $('#errorDiv span').text(response.data)
                $('.welcomeHeader').hide();
                NProgress.done();
             }
        });
};

function updateHTMLForNoHistory(data)
{
    $('.nohistorypresent').children().html(data);
    $('.nohistorypresent').removeClass("hide").addClass('show');
    showTabs();
    hideMoviesList();
}


function createData(data)
{
    vals = JSON.parse(data);
    myData = []
    $.each(vals[1],function(key,value)
    {
        temp = {} ;
        temp.sn = parseInt(key)+1;
        temp.id = vals[1][key];
        temp.movie = vals[2][key];
        myData.push(temp);
    });
    return myData;
}

function showTabs()
{
    $('#frame1').removeClass("hide").addClass('show');
    $('#frame2').removeClass("hide").addClass('show');
    showMoviesList();
    $('#tabs').removeClass("hide").addClass('show').addClass('fadeInAnimation');
}

function showLeftTab()
{
    $('#frame1').removeClass("hide").addClass('show');
    $('#tabs').removeClass("hide").addClass('show').addClass('fadeInAnimation');
}

function showRightTab()
{
    $('#frame2').removeClass("hide").addClass('show');
    showMoviesList();
    $('#tabs').removeClass("hide").addClass('show').addClass('fadeInAnimation');
}

function hideMoviesList()
{
    $('#movieListContainer').removeClass("show").addClass('hide');
}

function showMoviesList()
{
    $('#movieListContainer').removeClass("hide").addClass('show');
}

function updateHTML(data,name) {


     //data = createData(data);

    $.get("/static/html_templates/movieTemplate.html", null, function (movieTemplate) {

            // Render the books using the remote template
            $.tmpl(movieTemplate, data).appendTo("#movieTable tbody");
            $('tr:even:not(:first)').addClass('alt')
    });
}
