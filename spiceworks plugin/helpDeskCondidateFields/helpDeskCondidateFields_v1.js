/*
Category, Software License Requirements, Select a software;
Category, Hardware, Select A Hardware;
Office Location, Beijing, Beijing Projects;
Office Location, Beijing, Beijing Rooms;
Select A Hardware, HDD, Hdd Solution;
Department, HR, Hr Category;
Department, HR, Artist, PM, Office Location;
Department, Artist, PM, Previous Project;
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
            initialization : []
        },

        selectors : {},

        hideSubcategories : function (category) {
            var i, subcategory;
            
            if (APP.maps.hasOwnProperty(category)) {
                for (i=0; i<APP.maps[category].subsequence.length; i++) {
                    subcategory = APP.maps[category].subsequence[i].slice(-1)[0];
                    
                    $('select[id=' + APP.selectors[subcategory] + ']').prop('selectedIndex', 0);
                    $('li[id=' + APP.selectors[subcategory] + ']').hide(500);
                    APP.hideSubcategories(subcategory);
                }
            }
        },

        showSubcategories : function (category) {
            var i;
            var field;
            var subcategory;

            if (APP.maps.hasOwnProperty(category)) {
                for (i=0; i<APP.maps[category].subsequence.length; i++) {
                    field = $('select[id=' + APP.selectors[category] + ']').val();
                    subcategory = APP.maps[category].subsequence[i].slice(-1)[0];
    
                    if (APP.maps[category].subsequence[i].slice(0, -1).includes(field)) {
                        $('li[id=' + APP.selectors[subcategory] + ']').slideDown(500);
                        APP.showSubcategories(subcategory);
                    }
                }
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

                if (APP.maps.hasOwnProperty(_label)) {
                    $('select[id='+APP.selectors[_label] + ']').change(APP.toggleCategories);
                }
            }

            for (i=0; i<APP.maps.initialization.length; i++) {
                APP.showSubcategories(APP.maps.initialization[i]);
            }
        },

        initialize : function () {
            var i;
            var category;
            var settings = plugin.settings.ctree.split(';').slice(0, -1);

            for (i=0; i<settings.length; i++) {
                settings[i] = settings[i].split(',').map(function (field) {
                    return field.trim();
                });

                category = settings[i][0];
                if (APP.maps[category] === undefined) {
                    APP.maps[category] = {};
                    APP.maps[category].subsequence = [];
                }

                APP.maps[category].subsequence.push(settings[i].slice(1));
                APP.maps.subcategories.push(settings[i].slice(-1)[0]);
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