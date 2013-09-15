/*hg = typeof hg =='undefined'? {} : hg;

$(document).ready(function() {
    hg.int=self.setInterval(function(){updateprogress()},1000);
});

function updateprogress() {
    var val = ( 100 * parseFloat($('#progressbar').css('width')) / parseFloat($('#progressbar').parent().css('width')) );
    if ( val < 100 ) {
        val = val + 10;
        $('#progressbar').css({'width':val+'%'});
    } else {
        window.clearInterval(hg.int);
        $('#progressdiv').css({'visibility':'hidden'});
        $('#showmagicdiv').css({'visibility':'visible'});
    }
}*/