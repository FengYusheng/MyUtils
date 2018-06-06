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
            name: 'ctree',
            label: 'Categories',
            type: 'text',
            defaultValue: '',
            example:'Category,Value,Subcategory;Category,Value1,Value2,Subcategory etc.'
        }
    ]
});

var CANDIDATE;

plugin.includeStyles();

(function ($) {

    CANDIDATE = {
        VERSION : '0.1',

        debug : false,

        categories : [],

        defaultValues : {},

        userPortal : false,

        dbg : function (msg) {
            if (CANDIDATE.debug && console) {
                console.log('[Help Desk Candidate Fields]: ' + msg);
            }
        },

        // Execute the callback after loading the DOM object.
        ready : function (obj, callback) {
            setTimeout(function () {
                if ($(obj).length) {
                    callback();
                }
                else {
                    CANDIDATE.ready();
                }
            }, 10);
        },

        matchURL : function (path) {
            return location.pathname.includes(path);
        },

        // This function install our own setting html page.
        installPage : function () {
            setTimeout(function () {
                if (CANDIDATE.categories.length && CANDIDATE.userPortal) {
                    CANDIDATE.settings.app = $('.sw-app-name:contains("Mindwalk Help Desk Candidate Fields")').closest('.sw-app-row');
                    CANDIDATE.settings.init();
                }
                else {
                    CANDIDATE.installPage();
                }
            }, 10);
        },

        init : function () {
            // Get the custom attributes.
            $.getJSON('/api/custom_attributes', function (data) {
                var c;
                var attrs = data.custom_attributes;
                for (var i=0; i<attrs.length; i++) {
                    c = attrs[i].name.split('c_')[1].replace(/_/g, ' ').trim();
                    CANDIDATE.categories.push(c);
                    CANDIDATE.defaultValues[c] = attrs[i].default;
                }

                CANDIDATE.categories.sort();

                CANDIDATE.dbg(CANDIDATE.categories);
                CANDIDATE.dbg(CANDIDATE.defaultValues);

            });

            // Get user portal 
            // cross domain
            // dataType, Accepts in $.ajax : https://stackoverflow.com/questions/33060712/datatype-vs-accepts-ajax-request
            $.ajax({
                url : '/user_portal/custom_ticket_forms?element_id=custom-ticket-form_1527568538&end_user_mode=true&id=1',

                dataType : 'text', // Expect the server to return a text result.

                crossDomain : true,

                success : function (data) {
                    var t;
                    var ids = [];
                    var pageText = decodeURIComponent(encodeURIComponent(data));
                    // TODO: Extract labels from the user portal page.
                    // Get labels : \\u003Clabel\s*?for=\\"(custom_ticket_form_field_\d*?)\\"\s*?style=\\"\\"\\u003E(.*?)\\u003C/label
                    // Get ids : \\u003Cli\s*?class=\\"(.*?)\\"\s*?id=\\"(.*?)\\"\\u003E
                    var pattern = /\\u003Cli\s*?class=\\"(.*?)\\"\s*?id=\\"(.*?)\\"\\u003E/g;

                    // Skip custom attribute's ids.
                    var match = pattern.exec(pageText);
                    while (match) {
                        t = match[1].split(' ');
                        if (t[1].trim() === 'custom-form-field' && t[0].trim() !== 'custom-ticket-attribute-form-field') {
                            ids.push(match[2].trim());
                        }
                        match = pattern.exec(pageText);
                    }

                    // Extract the labels.
                    pattern = /\\u003Clabel\s*?for=\\"(custom_ticket_form_field_\d*?)\\"\s*?style=\\"\\"\\u003E(.*?)\\u003C\/label/g;
                    pattern = '\\\\u003Clabel\\s*?for=\\\\"' + ids[0] + '\\\"';
                    pattern = new RegExp(pattern, 'g');
                    console.log(pattern.exec(pageText));

                    CANDIDATE.userPortal = true;

                },
                
                error : function (r, d, e) {
                    console.log(d);
                }
            });

            if (CANDIDATE.matchURL('/settings')) {
                SPICEWORKS.observe('plugin:componentRendered', function () {
                    if (CANDIDATE.matchURL('/settings/apps')) {
                        CANDIDATE.installPage();
                    }
                });
            }
        },


        settings : {
            app : null,

            form : null,

            temp : [],

            validate : function () {
                var i;
                var v = [];
                var suspect = {};

                // White list.
                var rows = CANDIDATE.settings.app.find('#MWHDCF-white tr');
                var w_c, w_fields, w_sub;
                v = [];
                for (i=1; i<rows.length; i++) {
                    w_c = $(rows[i]).children(':first').text().trim();
                    w_fields = $(rows[i]).children(':nth-child(2)').text().trim();
                    w_sub = $(rows[i]).children(':nth-child(3)').text().trim();

                    if (!suspect.hasOwnProperty(w_c)) {
                        suspect[w_c] = {};
                        suspect[w_c].parent = [];
                    }

                    if (!suspect[w_c].parent.includes(w_sub)) {
                        if (!suspect.hasOwnProperty(w_sub)) {
                            suspect[w_sub] = {};
                            suspect[w_sub].parent = [];
                        }

                        if (!suspect[w_sub].parent.includes(w_c)) {
                            suspect[w_sub].parent.push(w_c);
                        }

                    }
                    else {
                        $(rows[i]).css('background-color', 'lightpink');
                        return false;
                    }
                    
                    $(rows[i]).css('background-color', 'inherit');

                    if (w_c !== 'None' && w_fields !== 'None' && w_sub !== 'None') {
                        v.push(w_c+','+w_fields+','+w_sub+', yes;');
                    }
                }
                
                // Black list.
                suspect = {};
                rows = CANDIDATE.settings.app.find('#MWHDCF-black tr');
                for (i=1; i<rows.length; i++) {
                    w_c = $(rows[i]).children(':first').text().trim();
                    w_fields = $(rows[i]).children(':nth-child(2)').text().trim();
                    w_sub = $(rows[i]).children(':nth-child(3)').text().trim();

                    if (!suspect.hasOwnProperty(w_c)) {
                        suspect[w_c] = {};
                        suspect[w_c].parent = [];
                    }

                    if (!suspect[w_c].parent.includes(w_sub)) {
                        if (!suspect.hasOwnProperty(w_sub)) {
                            suspect[w_sub] = {};
                            suspect[w_sub].parent = [];
                        }

                        suspect[w_sub].parent.push(w_c);
                    }
                    else {
                        $(rows[i]).css('background-color', 'lightpink');
                        return false;
                    }
                    
                    $(rows[i]).css('background-color', 'inherit');

                    if (w_c !== 'None' && w_fields !== 'None' && w_sub !== 'None') {
                        v.push(w_c+','+w_fields+','+w_sub+','+'no;');
                    }
                }

                CANDIDATE.settings.app.find('input[id^="ctree_"]').val(v.join(''));

                return true;
            },

            load : function (form) {
                var i, c;

                if ($('#MWHDCF').length) {
                    return;
                }
    
                // Before "save" and "cancel" buttons.
                $('<div id="MWHDCF"></div>').insertBefore(form.find('div:last'));
    
                plugin.renderHtmlTemplate('settings.html', {}, function(content) {
                    $('#MWHDCF').html(content);

                    // Adjust blue marker height
                    $('#sw-app-row-marker').animate({ height: $('.Mindwalk').height() - 5 }, 250);

                    // Initialize "Initial Categories" tab.
                    if (CANDIDATE.categories.length) {
                        for (i=0; i<CANDIDATE.categories.length; i++) {
                            c = CANDIDATE.categories[i];
                            $('#categories').append('<option value="' + c + '">' + c + '</option>');
                        }
                    }
                    else {
                        CANDIDATE.dbg('Failed to get custom attributes.');
                    }

                    $('#AddWhite').click(function () {
                        var n = '<tr class="MW-table-row">';
                        n += '<td class="MW-table-content category"><span>None</span></td>';
                        n += '<td class="MW-table-content fields"><span>None</span></td>';
                        n += '<td class="MW-table-content subcategory"><span>None</span></td>';
                        n += '<td class="MW-action-delete"><span>X</span></td>';
                        n += '</tr>';

                        $('#MWHDCF-white').children(':first').append(n);
                    });

                    $('#AddBlack').click(function () {
                        var n = '<tr class="MW-table-row">';
                        n += '<td class="MW-table-content category"><span>None</span></td>';
                        n += '<td class="MW-table-content fields"><span>None</span></td>';
                        n += '<td class="MW-table-content subcategory"><span>None</span></td>';
                        n += '<td class="MW-action-delete"><span>X</span></td>';
                        n += '</tr>';

                        $('#MWHDCF-black').children(':first').append(n);
                    });

                    $(document).on('click', 'td.MW-table-content span', function () {
                        var i, c, fields;
                        var p = $(this).parent();
                        var oldValue = $(this).text();

                        if (p.hasClass('category')) {

                            c = $(this).closest('.MW-table-row').children(':nth-child(3)').text().trim();
                            p.html('<select autofocus class="member"></select>');

                            for (i=0; i<CANDIDATE.categories.length; i++) {

                                if (c !== CANDIDATE.categories[i]) {

                                    if (oldValue === CANDIDATE.categories[i]) {
                                        p.children(':first').append( '<option selected="selected" value="' + CANDIDATE.categories[i] + '">' + CANDIDATE.categories[i] + '</option>' );
                                    }
                                    else{
                                        p.children(':first').append( '<option value="' + CANDIDATE.categories[i] + '">' + CANDIDATE.categories[i] + '</option>' );
                                    }

                                }
                            }
                            
                            $(this).parent().children('.subcategory').html('<span>None</span>');

                        }
                        else if (p.hasClass('fields')) {

                            if (oldValue !== '') {
                                oldValue = oldValue.split(',\n').join(',');
                            }

                            c = $(this).closest('.MW-table-row').children(':first').text().trim();
                            p.html('<textarea rows="20" cols="40" autofocus="" class="ember-view ember-text-area">' + oldValue + '</textarea>');

                        }
                        else if (p.hasClass('subcategory')) {
                            
                            c = $(this).closest('.MW-table-row').children(':first').text().trim();
                            p.html('<select autofocus class="member"></select>');

                            for (i=0; i<CANDIDATE.categories.length; i++) {
                                if (CANDIDATE.categories[i] !== c) {

                                    if (CANDIDATE.categories[i] === oldValue) {
                                        p.children(':first').append( '<option selected="selected" value="' + CANDIDATE.categories[i] + '">' + CANDIDATE.categories[i] + '</option>' );
                                    }
                                    else {
                                        p.children(':first').append( '<option value="' + CANDIDATE.categories[i] + '">' + CANDIDATE.categories[i] + '</option>' );
                                    }
                                }
                            }
                        }

                        p.children(':first').focus();
                    });

                    $(document).on('focusout', 'td.MW-table-content', function () {
                        var value;

                        if ($(this).hasClass('category')) {
                            value = $(this).children(':first').val();

                            if (value === '') {
                                value = 'None';
                            }

                            $(this).html('<span>' + value + '</span>');
                        }
                        else if ($(this).hasClass('fields')) {
                            value = $(this).children(':first').val();
                            
                            if (value === '') {
                                value = 'None';
                            }

                            value = value.split(',').join(',\n');
                            
                            $(this).html('<span>' + value + '</span>');
                        }
                        else if ($(this).hasClass('subcategory')) {
                            
                            value = $(this).children(':first').val();

                            if (value === '') {
                                value = 'None';
                            }

                            $(this).html('<span>' + value + '</span>');

                            // Validate the rules.
                            if(!CANDIDATE.settings.validate()) {
                                $('.sui-bttn-primary:contains("Add")').hide();
                                $('.sui-bttn-primary:contains("Save")').hide();
                            }
                            else {
                                $('.sui-bttn-primary:contains("Add")').show();
                                $('.sui-bttn-primary:contains("Save")').show();
                            }

                        }
                    });

                    $(document).on('click', '.MW-action-delete', function () {
                        $(this).closest('.MW-table-row').remove();
                        
                        // Validate the rules.
                        if(!CANDIDATE.settings.validate()) {
                            $('.sui-bttn-primary:contains("Add")').hide();
                            $('.sui-bttn-primary:contains("Save")').hide();
                        }
                        else {
                            $('.sui-bttn-primary:contains("Add")').show();
                            $('.sui-bttn-primary:contains("Save")').show();
                        }
                    });
                });
            },

            // This function fill the plugin.setting data into our setting html page.
            fillSettings : function () {
                // Fill initial category
                var i;
                var initials = plugin.settings.initial.split(';').slice(0, -1);
                
                if (initials.length && initials[0] === '') {
                    // BUG: initials[0] === ';'
                    initials = [];
                }

                // Fill white and black list.
                var rules = plugin.settings.ctree.split(';').slice(0, -1);
                var r, isBlack, category, fields, subcategory, tr;
                for (i=0; i<rules.length; i++) {
                    r = rules[i].split(',');
                    isBlack = r.slice(-1)[0] === 'no';
                    r = r.slice(0, -1);

                    category = r[0];
                    subcategory = r.slice(-1)[0];
                    fields = r.slice(1, -1);

                    tr = '<tr class="MW-table-row">';
                    tr += '<td class="MW-table-content category"><span>' + category +'</span></td>';
                    tr += '<td class="MW-table-content fields"><span>' + fields +'</span></td>';
                    tr += '<td class="MW-table-content subcategory"><span>' + subcategory + '</span></td>';
                    tr += '<td class="MW-action-delete"><span>X</span></td>';
                    tr += '</tr>';
                    
                    if (isBlack) {
                        CANDIDATE.settings.app.find('#MWHDCF-black tbody').append(tr);
                    }
                    else {
                        CANDIDATE.settings.app.find('#MWHDCF-white tbody').append(tr);
                    }
                }

                
            },

            // Check whether our own setting page has been installed.
            init : function () {
                if (CANDIDATE.settings.app.hasClass('Mindwalk')) {
                    return;
                }

                CANDIDATE.settings.app.addClass('Mindwalk');

                // Show logo.
                CANDIDATE.settings.app.find('.sw-app-icon.sw-app-icon-gradient>img').attr('src', plugin.contentUrl('MindwalkLogo.png'));

                // Replace the default setting page with our own page when the user clicks the "configure" link.
                CANDIDATE.settings.app.find('.sw-app-configure-link').on('mouseup', function () {
                    if (!CANDIDATE.settings.app.find('.plugin-configure').length) {
                        CANDIDATE.ready(
                            '.Mindwalk .plugin-configure > form', function () {
                                CANDIDATE.settings.form = CANDIDATE.settings.app.find('.plugin-configure > form');
                                CANDIDATE.settings.load(CANDIDATE.settings.form);
                                CANDIDATE.settings.fillSettings();
                            }
                        );
                    }
                });
            }
        }
    };

})(jQuery);



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

            if (APP.maps.blackList[category] !== undefined && APP.selectors[category] !== undefined) {
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

            if (APP.maps.whiteList[category] !== undefined && APP.selectors[category] !== undefined) {
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
            var category = $('label[for=' + id + ']').text().trim().slice(0, -1).toLowerCase();
            APP.hideSubcategories(category);
            APP.showSubcategories(category);
        },

        initializeSubcategories : function () {
            var i, _label, _category, selector;

            for (i=0; i<APP.labels.length; i++) {
                _label = APP.labels[i].text().trim().slice(0, -1).toLowerCase();
                APP.selectors[_label] = $(APP.labels[i]).parents('li.custom-ticket-attribute-form-field.custom-form-field').attr('id');
               
                if (APP.maps.subcategories.includes(_label)) {
                    $('li[id=' + APP.selectors[_label] + ']').hide();
                }

                if (APP.maps.whiteList.hasOwnProperty(_label) || APP.maps.blackList.hasOwnProperty(_label)) {
                    if (APP.selectors[_label] !== undefined) {
                        $('select[id='+APP.selectors[_label] + ']').change(APP.toggleCategories);
                    }
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
                /*Minimizing and restoring browser window makes browser send an ajax request. */
                APP.labels = $('label[for^=custom_ticket_form_field_]');
                APP.initializeSubcategories();
            }
           });
        }
    };
})(jQuery);



SPICEWORKS.app.ready(CANDIDATE.init);

SPICEWORKS.portalv2.ready(APP.initialize);