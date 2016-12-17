function loadPage() {

    loadData();
    $('#searchform').bind("submit",search);


}

function loadData()
 {
    NProgress.start();
    $userNameDiv = $('.welcomeHeader')[0];
     $('#searchListContainer').removeClass("show").addClass('hide');
      $('#historyListContainer').removeClass("show").addClass('hide');

    //hide search box
    $('#search').addClass('hide').removeClass('show');


    username = $userNameDiv.textContent.replace(" Welcome ","");
    userID = $userNameDiv.id;
    //show the header div
    $('.welcomeHeader').addClass('fadeInAnimation').show();
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
                showMoviesList();
                $('#historyListContainer').removeClass("show").addClass('hide');
                $('.logout').removeClass("hide").addClass('show');
                $('.tableHeading span').text('Top 10 Recommendations');
                $('.tableHeading').removeClass("hide").addClass('show');

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

function updateHTML(data,name)
{
     //data = createData(data);

    $.get("/static/html_templates/movieTemplate.html", null, function (movieTemplate) {

            // Render the books using the remote template
            $("#movieTable tbody").children().remove();
            $.tmpl(movieTemplate, data).appendTo("#movieTable tbody");
            $('tr:even:not(:first)').addClass('alt');
    });
}

function updateHistoryTable(data,nobatches,activeFooter)
{
    $('.tableHeading span').text('History');
    $('.tableHeading').removeClass("hide").addClass('show');

    $.get("/static/html_templates/movieHistoryTemplate.html", null, function (movieTemplate) {

            // Render the books using the remote template
            listData = $.tmpl(movieTemplate, data);
            $("#historyTable tbody").children().remove();
            $divtoAppend = $("#historyTable tbody")[0];
            $.each(listData, function(i,val) { $divtoAppend.appendChild(val); })
            $('tr:even:not(:first)').addClass('alt');
            $('#historyListContainer tfoot tr').removeClass('alt')
    });

    hideMoviesList();
    $('#historyListContainer tfoot ul').children().remove();
    $footerDiv = $('#historyListContainer tfoot ul')[0];
    $footerDiv.innerHTML += "<li onclick='getUserHistory(event)'><span>Previous</span></li>";
    $('#historyListContainer').removeClass("hide").addClass('show');
    for (i = 0 ; i < nobatches ; i ++ ) {
        htmlLiTag = "<li onclick='getUserHistory(event)'><span>" + (i+1) + "</span></li>"
        if (i== activeFooter-1) {htmlLiTag = "<li onclick='getUserHistory(event)' class='active'><span>" + (i+1) + "</span></li>"}
        $footerDiv.innerHTML += htmlLiTag;
    }
    $footerDiv.innerHTML += "<li onclick='getUserHistory(event)'><span>Next</span></li>";

}

function getUserHistory(ev)
{
    NProgress.start();
     $('#searchListContainer').removeClass("show").addClass('hide');

    //hide search box
    $('#search').addClass('hide').removeClass('show');

    ev.preventDefault();
    batchNo = 0;
    //if history button is clicked
    if ($(ev.toElement).hasClass('history') || $(ev.toElement).parent().hasClass('history')) {
        batchNo = 1
    }

    //if navigation buttons are clicked
    else if (ev.toElement.textContent.trim() == 'Previous') {
        $ulTag = $(ev.toElement).parents('ul');
        $newActiveTag = $ulTag.children('.active').prev();
        $activeTag = $ulTag.find('.active');
        if ($activeTag.text() == 1)
            batchNo = 1;
        else {
            batchNo = parseInt($activeTag.text().trim()) - 1;
            $activeTag.removeClass('active');
            $newActiveTag.addClass('active');
        }
    }

    else if (ev.toElement.textContent.trim() == 'Next') {
        $ulTag = $(ev.toElement).parents('ul');
        $newActiveTag = $ulTag.children('.active').next();
        $activeTag = $ulTag.find('.active');

        if ($newActiveTag.text().trim() == 'Next') {
            batchNo = parseInt($activeTag.text().trim());
        }
        else {
            batchNo = parseInt($activeTag.text().trim()) + 1;
            $activeTag.removeClass('active');
            $newActiveTag.addClass('active');
        }
    }

    else {
        $ulTag = $(ev.toElement).parents('ul');
        $newActiveTag = $(ev.toElement);
        $activeTag = $ulTag.find('.active');
        $activeTag.removeClass('active');
        $newActiveTag.addClass('active');
        batchNo = parseInt($(ev.toElement).text().trim());
    }

    $userNameDiv = $('.welcomeHeader')[0];
    userID = $userNameDiv.id;
    $.getJSON('/history', {
        userid:userID,
        batchno:batchNo,
        },
        function(response){
            if (response.status == -1) {
                updateHTMLForNoHistory(response.data);
                showLeftTab();
                NProgress.done();
            }
            else if (response.status) {
                updateHistoryTable(response.data,response.nobatches,batchNo)
                NProgress.done();
            }
            else {
                $('#errorDiv').show();
                $('#errorDiv span').text('Something went wrong')
                $('.welcomeHeader').hide();
                NProgress.done();
             }
        });


}

function updateHTMLForSearch(data,nobatches,activeFooter)
{
    $('.tableHeading span').text('Search Results');
    $('.tableHeading').removeClass("hide").addClass('show');


    $.get("/static/html_templates/searchMovieTemplate.html", null, function (movieTemplate) {

            // Render the books using the remote template
            listData = $.tmpl(movieTemplate, data);
            $("#searchTable tbody").children().remove();
            $divtoAppend = $("#searchTable tbody")[0];
            $.each(listData, function(i,val) { $divtoAppend.appendChild(val); })
            $('tr:even:not(:first)').addClass('alt');
            $('#searchListContainer tfoot tr').removeClass('alt')
    });

    $('#searchListContainer tfoot ul').children().remove();
    if (nobatches > 1)
    {
        $footerDiv = $('#searchListContainer tfoot ul')[0];
        $footerDiv.innerHTML += "<li onclick='search(event)'><span>Previous</span></li>";

        for (i = 0 ; i < nobatches ; i ++ ) {
            htmlLiTag = "<li onclick='search(event)'><span>" + (i+1) + "</span></li>"
            if (i== activeFooter-1) {htmlLiTag = "<li onclick='search(event)' class='active'><span>" + (i+1) + "</span></li>"}
            $footerDiv.innerHTML += htmlLiTag;
        }
        $footerDiv.innerHTML += "<li onclick='search(event)'><span>Next</span></li>";
    }
    $('#searchListContainer').removeClass("hide").addClass('show');
}

function searchClicked()
{
    $('#search').addClass('show').removeClass('hide');
    $('#search').find('h1').text('Search');
    $('#searchbox').val('');
    hideMoviesList();
    $('#historyListContainer').removeClass("show").addClass('hide');
    $('.tableHeading span').text('Search Results');
    $('.tableHeading').removeClass("show").addClass('hide');
    $('.nohistorypresent').removeClass("show").addClass('hide');
}

function updateHTMLForNoSearch(data)
{
    $('.tableHeading span').text(data);
    $('.tableHeading').removeClass("hide").addClass('show');
    $('#searchListContainer').removeClass("show").addClass('hide');
}


function search(ev)
{
    NProgress.start();
    searchText = $('#searchbox').val().trim();
    $('.tableHeading span').text('Search Results');

    ev.preventDefault();
    batchNo = 1; //default value
    if (ev.type == "submit")
    {
        batchNo=1;
    }
    //if navigation buttons are clicked
    else if (ev.toElement.textContent.trim() == 'Previous') {
        $ulTag = $(ev.toElement).parents('ul');
        $newActiveTag = $ulTag.children('.active').prev();
        $activeTag = $ulTag.find('.active');
        if ($activeTag.text() == 1)
            batchNo = 1;
        else {
            batchNo = parseInt($activeTag.text().trim()) - 1;
            $activeTag.removeClass('active');
            $newActiveTag.addClass('active');
        }
    }

    else if (ev.toElement.textContent.trim() == 'Next') {
        $ulTag = $(ev.toElement).parents('ul');
        $newActiveTag = $ulTag.children('.active').next();
        $activeTag = $ulTag.find('.active');

        if ($newActiveTag.text().trim() == 'Next') {
            batchNo = parseInt($activeTag.text().trim());
        }
        else {
            batchNo = parseInt($activeTag.text().trim()) + 1;
            $activeTag.removeClass('active');
            $newActiveTag.addClass('active');
        }
    }

    else {
        $ulTag = $(ev.toElement).parents('ul');
        $newActiveTag = $(ev.toElement);
        $activeTag = $ulTag.find('.active');
        $activeTag.removeClass('active');
        $newActiveTag.addClass('active');
        batchNo = parseInt($(ev.toElement).text().trim());
    }


    //if keyword is atleast 3 characters
    if (searchText.length > 2) {

        $.getJSON('/search', {
        searchtext:searchText,
        batchno:batchNo,
        },
        function(response){
            if (response.status == -1) {
                updateHTMLForNoSearch(response.data);
                NProgress.done();
            }
            else if (response.status) {
                updateHTMLForSearch(response.data,response.nobatches,batchNo)
                NProgress.done();
            }
            else {
                $('#errorDiv').show();
                $('#errorDiv span').text('Something went wrong')
                $('.welcomeHeader').hide();
                NProgress.done();
             }
        });

    }
    else
    {
        $('.tableHeading span').text('Please Input atleast 3 characters for search');
    $('.tableHeading').removeClass("hide").addClass('show');
    NProgress.done();
    }

    return false;
}

function showPopUp(ev)
{

    self = $(ev.toElement);
    movieID = self.parent()[0].id
    $popUpDiv  = $('.confirm');
    if ($popUpDiv.hasClass('show')) { $popUpDiv.addClass('hide').removeClass('show'); ev.stopPropagation(); return false;}
    $popUpDiv.find('h1').removeAttr('class');
    $popUpDiv.find('h1').text(self.text()).addClass(movieID);
    $popUpDiv.addClass('show').removeClass('hide');
    $('body').bind("click",closePopUp);
    ev.stopPropagation();
}

function closePopUp()
{
    $popUpDiv  = $('.confirm');
    if ($popUpDiv.hasClass('show')) { $popUpDiv.addClass('hide').removeClass('show'); }
    $('body').unbind("click");
}

function updateHistory(ev) {

    self = $(ev.toElement);
    liking = 1;

    if (self.text() == "No") {
        liking = -1;
    }

    $parentDiv = self.parent();
    movieID = $parentDiv.find('h1').attr('class')
    $userNameDiv = $('.welcomeHeader')[0];
    userID = $userNameDiv.id;

    $.getJSON('/updatehistory', {
        userid:userID,
        movieid:movieID,
        liking:liking,
        },
        function(response){
            if (response.status) {
                $('.historyconfirm').addClass('show').removeClass('hide');
                NProgress.done();
            }
            else {
                $('#errorDiv').show();
                $('#errorDiv span').text('Something went wrong')
                $('.welcomeHeader').hide();
                NProgress.done();
             }
        });
}

function okayClicked(ev)
{
    $('.historyconfirm').addClass('hide').removeClass('show');
}

function buildHistoryClicked()
{
    $('#search').addClass('show').removeClass('hide');
    $('#search').find('h1').text('Search Movie, click on results to tell me whether you liked the movie or not');
    $('#searchbox').val('');
    hideMoviesList();
    $('#historyListContainer').removeClass("show").addClass('hide');
    $('.tableHeading span').text('Search Results');
    $('.tableHeading').removeClass("show").addClass('hide');
    $('.nohistorypresent').removeClass("show").addClass('hide');
}