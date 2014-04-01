function close_message(){
  var items = $(".alert , .alert-warning , .alert-dismissable");
  console.log(items[0]);
  if(items!==null){
    $(items[0]).delay(2000).slideUp("slow", function(){
      items[0].remove();
      close_message();
    });
  }
}

function add_SML(obj, type){
  var temp_clothes = $("#template-area .add_clothes").text();
  var temp_shoes = $("#template-area .temp_shoes").text();
  var temp_customs = $("#template-area .temp_customs").text();
  
  if(type=="clothes")
    template = temp_clothes;
  else if (type=="shoes")
    template = temp_shoes;
  else
    template = temp_customs;

  var parent = $(obj).parent().parent().parent();
  var add = $(obj).parent().parent();
  var addHTML = $(add).html()
  $(add).remove();
  $(parent).append(template);
}

function get_details(){
  var rows = $("#details").children();
  var size1, size2, size3, size4, size5, size6;
  var postdata = {};
  for (var i=0;i<rows.length;i++)
  {
    columns = [];
    var size_list;
    if($(rows[i]).prop("class")=="size customs success"){
      size_list = [];
      for (var j=1;j<=6;j++) {
        size = $($($(rows[i]).children()[j]).children()[0]).val();
        size_list.push(size);
      }
    }else if($(rows[i]).prop("class")=="size success"){
      size_list = [];
      for (j=1;j<=6;j++) {
        size = $($(rows[i]).children()[j]).text();
        size_list.push(size);
      }
    }else if ($(rows[i]).prop("class")=="data"){
      d = {};
      d["number"] = $($($(rows[i]).children()[0]).children()[0]).val();
      d["description"] = $($($(rows[i]).children()[1]).children()[0]).val();
      d["retail"] = $($($(rows[i]).children()[9]).children()[0]).val();
      d["whole"] = $($($(rows[i]).children()[10]).children()[0]).val();
      d["total"] = $($($(rows[i]).children()[11]).children()[0]).val();
      d['columns'] = [];
      for(j=0;j<6;j++){
        col = {};
        col['size'] = size_list[j];
        col['amount'] = $($($(rows[i]).children()[j+2]).children()[0]).val();
        d['columns'].push(col);
      }
      postdata[d['number']] = d;
    }
  }
  console.log(JSON.stringify(postdata));
  $("#details-data").val(JSON.stringify(postdata));
  return false;
}