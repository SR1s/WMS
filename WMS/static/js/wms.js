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