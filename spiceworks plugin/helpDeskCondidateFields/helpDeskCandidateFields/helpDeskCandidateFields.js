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

var CANDIDATE;

plugin.includeStyles();

(function ($) {

    CANDIDATE = {
        VERSION : '0.1',

        debug : false,

        categories : [],

        defaultValues : {},

        initialCategories : ['category'],

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

        installPage : function () {
            setTimeout(function () {
                if (CANDIDATE.categories.length) {
                    CANDIDATE.settings.app = $('.sw-app-name:contains("Mindwalk Help Desk Candidate Fields")').closest('.sw-app-row');
                    CANDIDATE.settings.init();
                }
                else {
                    CANDIDATE.installPage();
                }
            }, 10);
        },

        // This function fill the plugin.setting data into our setting html page.
        fillSettings : function () {
            console.log(plugin.settings.initial);
            console.log(plugin.settings.ctree);
        },

        // This function install our own setting html page.
        init : function () {
            //  SPICEWORKS.data.query({'tickets' : {'class' : 'Ticket'}}, function (result) {
            //     $.each(result.tickets[0], function (key, value) {
            //         if (key.startsWith('c_')) {

            //             CANDIDATE.categories.push( key.split('c_')[1].replace(/_/g, ' ').trim() );

            //         }
            //     });
            // });

            // Get the custom attributes.
            $.getJSON('/api/custom_attributes', function (data) {
                var c;
                var attrs = data.custom_attributes;
                for (var i=0; i<attrs.length; i++) {
                    c = attrs[i].name.split('c_')[1].replace(/_/g, ' ').trim();
                    CANDIDATE.categories.push(c);
                    CANDIDATE.defaultValues[c] = attrs[i].default;
                }

                CANDIDATE.dbg(CANDIDATE.categories);
                CANDIDATE.dbg(CANDIDATE.defaultValues);

            });

            if (CANDIDATE.matchURL('/settings')) {
                SPICEWORKS.observe('plugin:componentRendered', function () {
                    if (CANDIDATE.matchURL('/settings/apps')) {
                        CANDIDATE.installPage();
                        CANDIDATE.fillSettings();
                    }
                });
            }
        },


        settings : {
            app : null,

            form : null,

            temp : [],

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

                    // Initialize "Inital Categories" tab.
                    if (CANDIDATE.categories.length) {
                        for (i=0; i<CANDIDATE.categories.length; i++) {
                            c = CANDIDATE.categories[i];
                            $('#categories').append('<option value="' + c + '">' + c + '</option>');
                        }

                        $('#categories option').dblclick(function () {
                            var v = $(this).val().trim();
                            $(this).css('background-color', 'cadetblue');
                            if (!CANDIDATE.initialCategories.includes(v)) {
                                CANDIDATE.initialCategories.push(v);
        
                                $('#initialCategories').append('<option value="' + v + '">' + v + '</option>');
                                $('label[for=initialCategories]').text('Initial Categories (' + String(CANDIDATE.initialCategories.length) + '): ');
                            }
                            
                        });
                    }
                    else {
                        CANDIDATE.dbg('Failed to get custom attributs.');
                    }

                    $('#initialCategories').dblclick(function () {
                        var i, options;
                        var v = $('#initialCategories option:selected').val();
    
                        if ( v !== 'category') {
                            $('#categories option:contains(' + v + ')').css('background-color', 'transparent');
                            $('#initialCategories option:selected').remove();
    
                            options = $('#initialCategories option');
                            CANDIDATE.initialCategories = ['category'];
    
                            for (i=1; i<options.length; i++) {
                               CANDIDATE.initialCategories[i] = $(options[i]).val().trim();
                            }
    
                            $('label[for=initialCategories]').text('Initial Categories (' + String(CANDIDATE.initialCategories.length) + '): ');
                        }
                    });

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

                        if (p.hasClass('category')) {

                            p.html('<select autofocus class="member"></select>');

                            for (i=0; i<CANDIDATE.categories.length; i++) {
                                p.children(':first').append( '<option value="' + CANDIDATE.categories[i] + '">' + CANDIDATE.categories[i] + '</option>' );
                            }
                            
                            $(this).parent().children('.subcategory').html('<span>None</span>');

                        }
                        else if (p.hasClass('fields')) {

                            c = $(this).closest('.MW-table-row').children(':first').text().trim();

                            // p.html('<input type="text"></input><select autofocus class="member" multiple="multiple"></select>');
                            
                            // if (CANDIDATE.defaultValues.hasOwnProperty(c)) {
                                
                            //     fields = CANDIDATE.defaultValues[c].split(',');

                            //     for (i=0; i<fields.length; i++) {
                            //         p.children(':last').append( '<option value="' + fields[i].trim() + '">' + fields[i].trim() + '</option>' );
                            //     }
                            // }

                            p.html('<input type="text">');

                        }
                        else if (p.hasClass('subcategory')) {
                            
                            c = $(this).closest('.MW-table-row').children(':first').text().trim();
                            p.html('<select autofocus class="member"></select>');

                            for (i=0; i<CANDIDATE.categories.length; i++) {
                                if (CANDIDATE.categories[i] !== c) {
                                    p.children(':first').append( '<option value="' + CANDIDATE.categories[i] + '">' + CANDIDATE.categories[i] + '</option>' );
                                }
                            }
                        }

                        p.children(':first').focus();
                    });

                    $(document).on('focusout', 'td.MW-table-content', function () {
                        var value;

                        if ($(this).hasClass('category')) {
                            value = $(this).children(':first').val();
                            $(this).html('<span>' + value + '</span>');
                        }
                        else if ($(this).hasClass('fields')) {
                            value = $(this).children(':first').val();
                            
                            if (value === '') {
                                value = 'None';
                            }

                            $(this).html('<span>' + value + '</span>');
                        }
                        else if ($(this).hasClass('subcategory')) {
                            
                            value = $(this).children(':first').val();
                            $(this).html('<span>' + value + '</span>');

                        }
                    });

                    $(document).on('click', '.MW-action-delete', function () {
                        $(this).closest('.MW-table-row').remove();
                    });

                    // $(document).on('dblclick', 'td.MW-table-content.fields select option', function () {

                    // });
                });
            },

            validate : function () {
                var i;
                var v = [];

                // Initial categories.
                $.each(CANDIDATE.settings.app.find('#initialCategories').children(), function (index, element) {
                    v.push($(element).val().trim());
                });

                CANDIDATE.settings.app.find('input[id^="initial_"]').text(v.join(';')+';');

                // White list.
                var rows = CANDIDATE.settings.app.find('#MWHDCF-white tr');
                var w_c, w_fields, w_sub;
                v = [];
                for (i=1; i<rows.length; i++) {
                    w_c = $(rows[i]).children(':first').text().trim();
                    w_fields = $(rows[i]).children(':nth-child(2)').text().trim();
                    w_sub = $(rows[i]).children(':nth-child(3)').text().trim();
                    
                    if (w_c !== 'None' && w_fields !== 'None' && w_sub !== 'None') {
                        v.push(w_c+','+w_fields+','+w_sub+';');
                    }
                }
                
                // Black list.
                rows = CANDIDATE.settings.app.find('#MWHDCF-black tr');
                for (i=1; i<rows.length; i++) {
                    w_c = $(rows[i]).children(':first').text().trim();
                    w_fields = $(rows[i]).children(':nth-child(2)').text().trim();
                    w_sub = $(rows[i]).children(':nth-child(3)').text().trim();
                    
                    if (w_c !== 'None' && w_fields !== 'None' && w_sub !== 'None') {
                        v.push(w_c+','+w_fields+','+w_sub+','+'no;');
                    }
                }

                CANDIDATE.settings.app.find('input[id^="ctree_"]').text(v);
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

                                // Validate the settings before save.
                                CANDIDATE.settings.app.find('.sui-bttn-primary:contains("Save")').on('mousedown', function (e) {
                                    CANDIDATE.settings.validate();
                                });
                            }
                        );
                    }
                });
            }
        }
    };

})(jQuery);

SPICEWORKS.app.ready(CANDIDATE.init);