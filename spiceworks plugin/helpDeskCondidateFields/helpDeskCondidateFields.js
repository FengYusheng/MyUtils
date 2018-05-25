/*
Category, Software License Requirements, Select a software, yes;
Category, Hardware, Select A Hardware, yes;
Office Location, Beijing, Beijing Projects, yes;
Office Location, Beijing, Beijing Rooms, yes;
Select A Hardware, HDD, Hdd Solution, yes;
Department, HR, Hr Category, yes;
Department, HR, Artist, PM, Office Location, yes;
Department, Artist, PM, Previous Project, yes;
Hr Category, SWAT Password Reset, Office Location, no;
*/

'use strict';

plugin.configure({
    settingDefinitions:[
        {
            name: 'initial',
            label: 'Initial Categories',
            type: 'text',
            defaultValue: '',
            example: 'Category1;Category2;'
        },
        
        {
            name: 'ctree',
            label: 'Categories',
            type: 'text',
            defaultValue: '',
            example:'Category,Value,Subcategory;Category,Value1,Value2,Subcategory etc.'
        }
    ]
});

var APP;

(function ($) {
    APP = {
        labels : null,

        maps : {
            subcategories : [],
            initialization : [],
            whiteList : {},
            blackList : {}
        },

        selectors : {},

        hideSubcategories : function (category) {
            var i, subcategory;
            
            if (APP.maps.whiteList.hasOwnProperty(category)) {
                for (i=0; i<APP.maps.whiteList[category].subsequence.length; i++) {
                    subcategory = APP.maps.whiteList[category].subsequence[i].slice(-1)[0];
                    
                    $('select[id=' + APP.selectors[subcategory] + ']').prop('selectedIndex', 0);
                    $('li[id=' + APP.selectors[subcategory] + ']').hide(500);
                    APP.hideSubcategories(subcategory);
                }
            }
        },

        hideSubcategoriesInBlackList : function (category) {
            var i;
            var field;
            var subcategory;

            if (APP.maps.blackList.hasOwnProperty(category)) {
                for (i=0; i<APP.maps.blackList[category].subsequence.length; i++) {
                    field = $('select[id=' + APP.selectors[category] + ']').val().trim();
                    subcategory = APP.maps.blackList[category].subsequence[i].slice(-1)[0];

                    if (APP.maps.blackList[category].subsequence[i].slice(0, -1).includes(field)) {
                        $('select[id=' + APP.selectors[subcategory] + ']').prop('selectedIndex', 0);
                        $('li[id=' + APP.selectors[subcategory] + ']').hide(500);
                        APP.hideSubcategories(subcategory);
                    }
                    else if(!APP.maps.whiteList.hasOwnProperty(category)) {
                        $('li[id=' + APP.selectors[subcategory] + ']').slideDown(500);
                        APP.showSubcategories(subcategory);
                    }
                }
            }
        },

        showSubcategories : function (category) {
            var i;
            var field;
            var subcategory;

            if (APP.maps.whiteList.hasOwnProperty(category)) {
                for (i=0; i<APP.maps.whiteList[category].subsequence.length; i++) {
                    field = $('select[id=' + APP.selectors[category] + ']').val().trim();
                    subcategory = APP.maps.whiteList[category].subsequence[i].slice(-1)[0];
    
                    if (APP.maps.whiteList[category].subsequence[i].slice(0, -1).includes(field)) {
                        $('li[id=' + APP.selectors[subcategory] + ']').slideDown(500);
                        APP.showSubcategories(subcategory);
                    }
                }
            }

            if (APP.maps.blackList.hasOwnProperty(category)) {
                APP.hideSubcategoriesInBlackList(category);
            }
        },

        toggleCategories : function () {
            var id = $(this).attr('id');
            var category = $('label[for=' + id + ']').text().trim().slice(0, -1);

            APP.hideSubcategories(category);
            APP.showSubcategories(category);
        },

        initializeSubcategories : function () {
            var i, _label, _category, selector;

            for (i=0; i<APP.labels.length; i++) {
                _label = APP.labels[i].text().trim().slice(0, -1);
                APP.selectors[_label] = $(APP.labels[i]).parents('li.custom-ticket-attribute-form-field.custom-form-field').attr('id');
               
                if (APP.maps.subcategories.includes(_label)) {
                    $('li[id=' + APP.selectors[_label] + ']').hide();
                }

                if (APP.maps.whiteList.hasOwnProperty(_label) || APP.maps.blackList.hasOwnProperty(_label)) {
                    $('select[id='+APP.selectors[_label] + ']').change(APP.toggleCategories);
                }
            }

            for (i=0; i<APP.maps.initialization.length; i++) {
                APP.showSubcategories(APP.maps.initialization[i]);
            }

            for (i=0; i<APP.maps.initialization.length; i++) {
                if (APP.maps.blackList.hasOwnProperty( APP.maps.initialization[i] )) {
                    APP.hideSubcategoriesInBlackList( APP.maps.initialization[i] );
                }
            }

        },

        initialize : function () {
            var i;
            var category;
            var isBlack;
            var settings = plugin.settings.ctree.split(';').slice(0, -1);

            for (i=0; i<settings.length; i++) {
                settings[i] = settings[i].split(',').map(function (field) {
                    return field.trim();
                });

                category = settings[i][0];
                isBlack = settings[i].slice(-1)[0] === 'no';

                if (isBlack && !APP.maps.blackList.hasOwnProperty(category)) {
                    APP.maps.blackList[category] = {};
                    APP.maps.blackList[category].subsequence = [];
                }
                else if(!APP.maps.whiteList.hasOwnProperty(category)) {
                    APP.maps.whiteList[category] = {};
                    APP.maps.whiteList[category].subsequence = [];
                }

                if (isBlack) {
                    APP.maps.blackList[category].subsequence.push(settings[i].slice(1, -1));
                }
                else {
                    APP.maps.whiteList[category].subsequence.push(settings[i].slice(1, -1));
                }

                 APP.maps.subcategories.push(settings[i].slice(-2, -1)[0]);
            }

            APP.maps.initialization = plugin.settings.initial.split(';').slice(0, -1).map(function (c) {
                return c.trim();
            });

            /*$(document).ajaxComplete() doesn't handle ajax event here. */
           document.observe('ajax:completed', function () {
            if (APP.labels === null) {
                /*Minimizing and restoring browser window makes browser send an ajax requset. */
                APP.labels = $('label[for^=custom_ticket_form_field_]');
                APP.initializeSubcategories();
            }
           });
        }
    };
})(jQuery);


SPICEWORKS.portalv2.ready(APP.initialize);
