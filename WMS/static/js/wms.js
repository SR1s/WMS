function close_message(){
  var items = $(".message>.item");
  console.log(items[0]);
  if(items!=null){
    $(items[0]).delay(2000).slideUp("slow", function(){
      items[0].remove();
      close_message();
    });
  }
}

function add_SML(obj){
  var template = '<tr class="size"><td colspan="2"></td><td width="5%">XS</td><td width="5%">S</td><td width="5%">M</td><td width="5%">L</td><td width="5%">XL</td><td width="5%">XXL</td><td colspan="4"></td></tr><tr class="data"><td><input type="text" /></td><td><input type="text" /></td><td><input type="text" /></td><td><input type="text" /></td><td><input type="text" /></td><td><input type="text" /></td><td><input type="text" /></td><td><input type="text" /></td><td></td><td><input type="text" /></td><td><input type="text" /></td><td><input type="text" /></td></tr><tr><td colspan="12"><button type="button" onclick="add_SML(this)">Add new Size row</button></td></tr>';
  var parent = $(obj).parent().parent().parent();
  var add = $(obj).parent().parent();
  var addHTML = $(add).html()
  $(add).remove();
  $(parent).append(template);
}

function get_details(){
  var data = $("#details").children();
  var size1, size2, size3, size4, size5, size6;
  var postdata = new Array();
  for (var i=0;i<data.length;i++)
  {
    if($(data[i]).prop("class")=="size"){
      size1 = $($(data[i]).children()[1]).text();
      size2 = $($(data[i]).children()[2]).text();
      size3 = $($(data[i]).children()[3]).text();
      size4 = $($(data[i]).children()[4]).text();
      size5 = $($(data[i]).children()[5]).text();
      size6 = $($(data[i]).children()[6]).text();
    }else if ($(data[i]).prop("class")=="data"){
      d = new Object();
      d["number"] = $($($(data[i]).children()[0]).children()[0]).val();
      d["description"] = $($($(data[i]).children()[1]).children()[0]).val();
      d["size1"] = size1;
      d["size2"] = size2;
      d["size3"] = size3;
      d["size4"] = size4;
      d["size5"] = size5;
      d["size6"] = size6;
      d['amount1'] = $($($(data[i]).children()[2]).children()[0]).val();
      d['amount2'] = $($($(data[i]).children()[3]).children()[0]).val();
      d['amount3'] = $($($(data[i]).children()[4]).children()[0]).val();
      d['amount4'] = $($($(data[i]).children()[5]).children()[0]).val();
      d['amount5'] = $($($(data[i]).children()[6]).children()[0]).val();
      d['amount6'] = $($($(data[i]).children()[7]).children()[0]).val();
      d["retail"] = $($($(data[i]).children()[9]).children()[0]).val();
      d["whole"] = $($($(data[i]).children()[10]).children()[0]).val();
      d["total"] = $($($(data[i]).children()[11]).children()[0]).val();
      postdata.push(d);
    }
  }
  console.log(JSON.stringify(postdata));
  $("#details-data").val(JSON.stringify(postdata));
}