// ==SPICEWORKS-PLUGIN==
// @name          Nested Ticket Attributes
// @description   This plugin will hide or show ticket attributes to create the illusion of nested attributes for your ticketing system.
// @version       2.4
// @author        Jim Kubicek (Original Plugin by: Paul Price)
// ==/SPICEWORKS-PLUGIN==
plugin.includeStyles();
plugin.configure({
  settingDefinitions:[
    { name:'ctree', label:'Categories', type:'text', defaultValue:'', example:'Category,Value,Subcategory;Category,Value1,Value2,Subcategory etc.'},
    { name:'cat', label:'Cat', type:'text', defaultValue:'', example:'This will trigger the dropdown chains.'},
    { name:'rtree', label:'Region', type:'text', defaultValue:'', example:'Region,Value,SubRegion;Region,Value1,Value2,SubRegion etc.'},
    { name:'rcat', label:'RCat', type:'text', defaultValue:'', example:'This will trigger the dropdown chains.'},
    { name:'ctreeAdmin', label:'Admin Categories (not visible on Portal)', type:'text', defaultValue:'', example:'Enter the Configuration String for the subcategories not visible on the portal. Category,Value,Subcategory;Category,Value1,Value2,Subcategory etc.'},
    { name:'bCatSub', label:'Use Category as a Sub', type:'checkbox', defaultValue: false, example:'Use the built in Category as a subcategory (if you have a custom attribute called "category", the custom attribute cannot be used as a sub)'},
    { name:'tEdit', label:'Use Subs?', type:'checkbox', defaultValue: false, example:'Use subcategories when editing tickets?'},
    { name:'remUnused', label:'Remove Unused', type:'checkbox', defaultValue: false, example:'Remove unused subcategories from the list of categories on ticket status page of the portal?'},
    { name:'defaultV', label:'Default Value', type:'string', defaultValue:'not provided', example: 'Enter the default value of the custom attribute you would like to be hidden from the ticket status page on the portal. (Does nothing if "Remove Unused" is not checked)' }

  ]
});

var cat = plugin.settings.cat.toLowerCase();
var lblcat = plugin.settings.cat+':';  

var rcat= plugin.settings.rcat.toLowerCase();
var lblrcat = plugin.settings.rcat+':';  

function SubCat(){
  var sub = plugin.settings.ctree.toLowerCase().split(';');
  var category = $('ticket_category');


  for (i=0;i<sub.length;i++){
    sub[i]=sub[i].split(',');

    var cWatch=$("ticket_c_" + sub[i][0].replace(/ /g, "_"));
    if (sub[i][0]==cat ){
      cWatch=category;
   }

    var trigger=false;
    var action=$("ticket_c_" + sub[i].last().replace(/ /g, "_"));
    if (plugin.settings.bCatSub ===true && sub[i].last().replace(/ /g, "_") == cat ){
      action = $('ticket_category');
    }
    for (t=1;t<sub[i].length-1;t++){
      if (cWatch.value.toLowerCase()==sub[i][t]){
        trigger=true;
        break;
      }
    }
    if (trigger===false){  
      $(action.parentNode).hide();
      action.value = '';
      action.selectedIndex=0;
  }
    if (trigger===true){
      cWatch.parentNode.parentNode.insertBefore(action.parentNode,cWatch.parentNode.nextSibling);
      $(action.parentNode).show();
      }



  }
}

function SubCatHDT(){
  var sub = plugin.settings.ctree.toLowerCase().split(';');

  if (plugin.settings.ctreeAdmin.toLowerCase() !== ''){
  var sub1 = plugin.settings.ctree.toLowerCase().split(';');
  var sub2 = plugin.settings.ctreeAdmin.toLowerCase().split(';');
  sub = sub1.concat(sub2);
}

  var nRow=1;
   var category = $('ticket_category');
  for (i=0;i<sub.length;i++){
     sub[i]=sub[i].split(',');

    //console.log(sub[i]+"=");
    var cWatch=$("ticket_c_" + sub[i][0].replace(/ /g, "_"));

     if (sub[i][0]==cat ){
       cWatch=category;
    }
    var trigger=false;
    var action=$("ticket_c_" + sub[i].last().replace(/ /g, "_"));
   if (plugin.settings.bCatSub ===true && sub[i].last().replace(/ /g, "_") == cat ){
      action = $('ticket_category');
    }
    for (t=1;t<sub[i].length-1;t++){
      if (cWatch.value.toLowerCase()==sub[i][t]){
        trigger=true;
        break;
      }
   }
    if (trigger===false){
        action.value = '';
        action.selectedIndex=0;
      $(action.parentNode).hide();
      $(action.parentNode).previous().hide();
      }
    if (trigger===true && $(cWatch.parentNode.previous()) == $(cWatch.parentNode.parentNode.childNodes[1]) || trigger===true && nRow===0 ){


      cWatch.parentNode.parentNode.insertBefore(action.parentNode.previous(),cWatch.parentNode.nextSibling);
      cWatch.parentNode.parentNode.insertBefore(action.parentNode,cWatch.parentNode.nextSibling.nextSibling);
      $(action.parentNode).show();
      $(action.parentNode).previous().show();
      nRow=1;
    } else if (trigger===true && $(cWatch.parentNode.previous()) != $(cWatch.parentNode.parentNode.childNodes[1])){
      var tr = document.createElement('tr');
      tr.appendChild(action.parentNode.previous());
      tr.appendChild(action.parentNode);

      cWatch.parentNode.parentNode.parentNode.insertBefore(tr,cWatch.parentNode.parentNode.nextSibling);
      $(action.parentNode).show();
      $(action.parentNode).previous().show();
      nRow=0;
    }
     }
}

function SubCatNT(){

  // var sub = plugin.settings.ctree.toLowerCase().split(';');
  var sub = plugin.settings.ctree.toLowerCase().split(';');

  if (plugin.settings.ctreeAdmin.toLowerCase() !== ''){
  var sub1 = plugin.settings.ctree.toLowerCase().split(';');
  var sub2 = plugin.settings.ctreeAdmin.toLowerCase().split(';');
  sub = sub1.concat(sub2);
}
   var category = $('ticket_form').getElementsByTagName('label');
    for (i=0;i<category.length;i++){
      if (category[i].innerHTML == lblcat ){
               category = category[i].next();
        break;
          }
    }

  for (i=0;i<sub.length;i++){
     sub[i]=sub[i].split(',');

    var cWatch=$("c_" + sub[i][0].replace(/ /g, "_") + "_popup");

      if (sub[i][0]==cat){
       cWatch=category;
    }

    var trigger=false;
    var action=$("c_" + sub[i].last().replace(/ /g, "_") + "_popup");
   if (plugin.settings.bCatSub ===true && sub[i].last().replace(/ /g, "_") == cat){
      action = $('ticket_form').getElementsByTagName('label');
     for (c=0;c<action.length;c++){
      if (action[c].innerHTML == lblcat ){
               action = action[c].next();
        break;
          }
    }
    }
    for (t=1;t<sub[i].length-1;t++){
      if (cWatch.value.toLowerCase()==sub[i][t]){
        trigger=true;
        break;
      }
   }
    if (trigger===false){
      if(action.parentNode)
        $(action.parentNode).hide();
      action.value = '';
      action.selectedIndex=0;
      }
    if (trigger===true){
      cWatch.parentNode.parentNode.insertBefore(action.parentNode,cWatch.parentNode.nextSibling);
      $(action.parentNode).show();     
        }    
  }
}

function clickedNT(){
 // var sub = plugin.settings.ctree.toLowerCase().split(';');
  var sub = plugin.settings.ctree.toLowerCase().split(';');

  if (plugin.settings.ctreeAdmin.toLowerCase() !== ''){
  var sub1 = plugin.settings.ctree.toLowerCase().split(';');
  var sub2 = plugin.settings.ctreeAdmin.toLowerCase().split(';');
  sub = sub1.concat(sub2);
}
  var category = $('ticket_form').getElementsByTagName('label');
    for (i=0;i<category.length;i++){
      if (category[i].innerHTML == lblcat ){
               category = category[i].next();
        break;
          }
    }
  for (i=0;i<sub.length;i++){
    sub[i]=sub[i].split(',');

    var cWatch=$("c_" + sub[i][0].replace(/ /g, "_") + "_popup");
    if (sub[i][0]==cat){
      cWatch=category;
   }
    var watched = "false";
    for (s=i-1;s>0;s--){
      var sameCat = sub[s][0];
      if  (sameCat==sub[i][0]){
        watched="true";
        break;        
      }
    }

          if (watched !=="true"){
            Event.observe(cWatch, 'change', SubCatNT);
          }
  }
}


function NTFormCheck(){
     document.stopObserving('ajax:completed', NTFormCheck);

  if ($("ticket_form")){
   clickedNT();
   SubCatNT();
   document.observe('ajax:completed', NTFormCheck);
    }
    else{
      document.observe('ajax:completed', NTFormCheck);
        }
  }


function NTToolBar(){
  document.observe('ajax:completed', NTFormCheck);
}

function SubCatHD(){

  NTToolBar();
  if (plugin.settings.tEdit === true) {
    SubCatHDT();
  }
   }

function clicked(){
  var sub = plugin.settings.ctree.toLowerCase().split(';');
   var category = $('ticket_category');
  for (i=0;i<sub.length;i++){
    sub[i]=sub[i].split(',');

    var cWatch=$("ticket_c_" + sub[i][0].replace(/ /g, "_"));
    if (sub[i][0]==cat){
      cWatch=category;
   }
    var watched = "false";
    for (s=i-1;s>0;s--){
      var sameCat = sub[s][0];
      if  (sameCat==sub[i][0]){
        watched="true";
        break;        
      }
    }
          if (watched !=="true"){
            Event.observe(cWatch, 'change', SubCat);
          }
  }
}
function clickedHD(){
  //var sub = plugin.settings.ctree.toLowerCase().split(';');
  var sub = plugin.settings.ctree.toLowerCase().split(';');

  if (plugin.settings.ctreeAdmin.toLowerCase() !== ''){
  var sub1 = plugin.settings.ctree.toLowerCase().split(';');
  var sub2 = plugin.settings.ctreeAdmin.toLowerCase().split(';');
  sub = sub1.concat(sub2);
}

   var category = $('ticket_category');
  for (i=0;i<sub.length;i++){
    sub[i]=sub[i].split(',');

    var cWatch=$("ticket_c_" + sub[i][0].replace(/ /g, "_"));
    if (sub[i][0]==cat){
      cWatch=category;
   }
    var watched = "false";
    for (s=i-1;s>0;s--){
      var sameCat = sub[s][0];
      if  (sameCat==sub[i][0]){
        watched="true";
        break;       
      }
    }
          if (watched !=="true"){
            Event.observe(cWatch, 'change', SubCatHDT);
          }
  }
}

function hideAtts(){
  var findAtts = document.getElementsByTagName('p');
  var remove = plugin.settings.defaultV.replace(/ /g, "_");
  remove = new RegExp("<strong>\\w*?<\\/strong>:\\&nbsp;"+ remove + ",|,\\S<strong>\\w*?<\\/strong>:\\&nbsp;" + remove, "gi");
       for (i=0;i<findAtts.length;i++){

        if ($(findAtts[i]).className == "ticket-custom-fields"){
          findAtts[i].innerHTML = findAtts[i].innerHTML.replace(/ /g,"_");
        findAtts[i].innerHTML = findAtts[i].innerHTML.replace(/<strong>\w*?<\/strong>:\&nbsp;not_provided,|,\S<strong>\w*?<\/strong>:\&nbsp;not_provided|<strong>\w*?<\/strong>:\&nbsp;not_provided/gi, "");
        findAtts[i].innerHTML = findAtts[i].innerHTML.replace(remove, "");
         findAtts[i].innerHTML = findAtts[i].innerHTML.replace(/_/g," ");
             }
      }

    }


//====================

function SubCat1()
{

  var sub = plugin.settings.rtree.toLowerCase().split(';');
  var category = $('ticket_c_region');


  for (i=0;i<sub.length;i++)
  {
    sub[i]=sub[i].split(',');

    var cWatch=$("ticket_c_" + sub[i][0].replace(/ /g, "_"));
    if (sub[i][0]==rcat )
    {
      cWatch=category;
    }

    var trigger=false;
    var action=$("ticket_c_" + sub[i].last().replace(/ /g, "_"));
    if (plugin.settings.bCatSub ===true && sub[i].last().replace(/ /g, "_") == rcat )
    {
      action = $('ticket_c_region');
    }
    for (t=1;t<sub[i].length-1;t++){
      if (cWatch.value.toLowerCase()==sub[i][t]){
        trigger=true;
        break;
      }
    }
    if (trigger===false){
      $(action.parentNode).hide();
      action.value = '';
      action.selectedIndex=0;
  }
    if (trigger===true){
      cWatch.parentNode.parentNode.insertBefore(action.parentNode,cWatch.parentNode.nextSibling);
      $(action.parentNode).show();
      }



  }
}

function clicked1(){
  var sub = plugin.settings.rtree.toLowerCase().split(';');
   var category = $('ticket_c_region');
  for (i=0;i<sub.length;i++){
    sub[i]=sub[i].split(',');

    var cWatch=$("ticket_c_" + sub[i][0].replace(/ /g, "_"));
    if (sub[i][0]==rcat){
      cWatch=category;
   }
    //console.log(sub[i][0]);
    var watched = "false";
    for (s=i-1;s>0;s--){
      var sameCat = sub[s][0];
      if  (sameCat==sub[i][0]){
        watched="true";
        break;
      }
    }
          if (watched !=="true"){
            Event.observe(cWatch, 'change', SubCat1);
          }
  }
}


function processcustomform()
{

  setTimeout(

    function aa()
    {

      var forms = document.forms;

      for(var i in forms)
      {
        var form = forms[i];
        var index = ($(form).id)?($(form).id).indexOf("custom_ticket_form"):-1;
        //console.log(index);
        if( index !== -1 )
        {

          console.log(($(form).id));
          break;
        }
      }

    }
  ,5000
  );

}


SPICEWORKS.portalv2.ready(clicked1);
SPICEWORKS.portalv2.ready(SubCat1);
SPICEWORKS.portalv2.ready(processcustomform);

//===================




SPICEWORKS.portalv2.ready(clicked);
SPICEWORKS.portalv2.ready(SubCat);
SPICEWORKS.app.helpdesk.ticket.ready(SubCatHD);
if (plugin.settings.tEdit === true) {
  SPICEWORKS.app.helpdesk.ticket.ready(clickedHD);
}
if (plugin.settings.remUnused === true){
  SPICEWORKS.portalv2.ready(hideAtts);
}
SPICEWORKS.app.ready(NTToolBar);


// Category,Mindwalk Tickets,Mindwalk Tickets;
// Category,Redhot Tickets,Redhot Tickets;
// Mindwalk Tickets,Mindwalk Projects,Mindwalk Projects;
// Mindwalk Projects,002_T8MNG(131_ARC),Athena(Roar),B166ER(SEDNA),Bear(Animator),Bear(Character),Black(Pecos),Cardinal(Relic),Claymore(Ice Cream),Confucius(Ice Cream),D3T(911),Dreadnaught(Stag),Dylan(FB),Fang(Green),FP(Funplus),Frost(Solution),Gander(Pancakes),Ghost(NFS Test),GOG(Pecos),Halifax (Pancakes),HongKong(Spark),HZ(XiShanJu),Joplin(FB),Madness(Birdman),Magnesium(Ice Cream),Mesa(Curry),Myth(Penguin),Nuke(Cage),Pancake(Ether),Phoenix (Elex),Pick(Pecos),Redsox(Posh),Respawn(Rise),Ronin(Pecos),SDM(Mindwalk),Siberia(Outpost),SnakeBite(Mountain),Snowman(Kilo),Sparta(Pancakes),Tall (Curry),TBD(Hero),Tire(KingKong),Washington(Gladiator),Wind(Redmid),Yellow(Gladiator),Training,Mindwalk Rooms;
// Mindwalk Rooms,Blue Room,Green Room,Yellow Room,Purple Room,Black Room,Brown Room,Moon1F,Moon2F,Tickets Option;
// Tickets Option,Software,Software;
// Software,License,license;Tickets Option,Employee,Employee Status;
// Employee Status,New Employee,Employee Movement,Employee Exit,HDD Solution;
// HDD Solution,NewClone,Reclone,Storage,keep Currently,AD DHCP Firewall Checked;
// AD DHCP Firewall Checked,Yes,Employee Number;