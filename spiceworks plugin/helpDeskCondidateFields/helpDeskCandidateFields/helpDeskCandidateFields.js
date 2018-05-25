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

        debug : true,

        categories : [],

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

        init : function () {
             SPICEWORKS.data.query({'tickets' : {'class' : 'Ticket'}}, function (result) {
                $.each(result.tickets[0], function (key, value) {
                    if (key.startsWith('c_')) {

                        CANDIDATE.categories.push( key.split('c_')[1].replace(/_/g, ' ').trim() );

                    }
                });
            });

            if (CANDIDATE.matchURL('/settings')) {
                SPICEWORKS.observe('plugin:componentRendered', function () {
                    if (CANDIDATE.matchURL('/settings/apps')) {
                        CANDIDATE.settings.app = $('.sw-app-name:contains("Mindwalk Help Desk Candidate Fields")').closest('.sw-app-row');
                        CANDIDATE.settings.init();
                    }
                });
            }
        },

        settings : {
            app : null,

            form : null,

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
                });
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
                            }
                        );
                    }
                });
            }
        }
    };

})(jQuery);

SPICEWORKS.app.ready(CANDIDATE.init);