plugin.configure({
    settingDefinitions:[
      { name:'ctree', label:'Categories', type:'text', defaultValue:'', example:'Category,Value,Subcategory;Category,Value1,Value2,Subcategory etc.'},
      { name:'ctreeAdmin', label:'Admin Categories (not visible on Portal)', type:'text', defaultValue:'', example:'Enter the Configuration String for the subcategories not visible on the portal. Category,Value,Subcategory;Category,Value1,Value2,Subcategory etc.'},
      { name:'bCatSub', label:'Use Category as a Sub', type:'checkbox', defaultValue: false, example:'Use the built in Category as a subcategory (if you have a custom attribute called "category", the custom attribute cannot be used as a sub)'},
      { name:'tEdit', label:'Use Subs?', type:'checkbox', defaultValue: false, example:'Use subcategories when editing tickets?'},
      { name:'remUnused', label:'Remove Unused', type:'checkbox', defaultValue: false, example:'Remove unused subcategories from the list of categories on ticket status page of the portal?'},
      { name:'defaultV', label:'Default Value', type:'string', defaultValue:'not provided', example: 'Enter the default value of the custom attribute you would like to be hidden from the ticket status page on the portal. (Does nothing if "Remove Unused" is not checked)' }
      
    ]
  });