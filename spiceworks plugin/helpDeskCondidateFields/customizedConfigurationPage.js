'use strict';

plugin.configure({
    settingDefinitions:[
      { name:'data', label:'Data:', type:'text', defaultValue:'' },
      { name:'users', label:'Users:', type:'text', defaultValue:'' },
      { name:'hash', label:'Hash:', type:'text', defaultValue:'' }
    ]
  });

  
  var PR;

  // Load CSS
  plugin.includeStyles();

  (function ($) {

    PR = {

        debug : true,

        data : [],

        // Display debug messages in console
        dbg : function(msg) {
            if (PR.debug && console) {
                console.log('[pepper-rorles] ' + msg);
            }
        },

        // Execute a callback function when a DOM object finishes loading
        ready : function (obj, callback) {
            setTimeout(function () {
                if ($(obj).length) {
                    callback();
                }
                else {
                    PR.ready(obj, callback);
                }
            }, 10);
        },

        // Match URL
        matchURL : function (path) {
            return (location.href.indexOf(path) !== -1);
        },

        // Plugin init
        init : function () {
            if (PR.matchURL('/portal')) {

            }

            if (SPICEWORKS.app.user && SPICEWORKS.app.user.role === 'admin') {
                // Load plugin data. The data is in JSON format.
                PR.data = plugin.settings.data;
                PR.data = (PR.data === '[]' || !PR.data) ? [] : $.parseJSON(PR.data);

                // GLobal Events
                $('body').on('click', '#pr-modal-override :checkbox', function () {
                    $(this).parent().next().toggle();
                });

                // CONVERT PERMISSION PATHS INTO AN ARRAY
                // $.each(array, callback);

                // CHECK PERMISSIONS ON HYPERLINKS
                if (PR.matchURL('/settings')) {
                    // EVENT: Plugin list refreshed
                    SPICEWORKS.observe('plugin:componentRendered', function () {
                        if (PR.matchURL('/settings/apps')) {
                            // Get your plugin in /settings/apps. closest() travels up the DOM tree until it finds a match for the 
                            // supplied selector.
                            PR.settings.app = $('.sw-app-name:contains("Custom Configuration Page")').closest('.sw-app-row');
                            PR.settings.init();
                        }
                    })
                }
            }


        },

        settings : {
            app : null,

            // Init plugin settings
            init : function () {
                // Determeine whether the html page has been installed.
                if (PR.settings.app.hasClass('pr')) {
                    return;
                }

                PR.settings.app.addClass('pr');

                // Show app logo (override default icon)
                var logo = PR.settings.app.find('.sw-app.incon > img');
                logo.attr('src', plugin.contentUrl('logo.png'));

                // Get Admin users.
                // I don't find any reference document about this kind of api.
                SPICEWORKS.data.query({'data': {'class' : 'User', 'conditions' : 'role="admin"'}}, function(users) {
                    PR.users = users.data;
                });

                // Event: show plugin settings
                // Get the "configure" href.
                var configLink = PR.settings.app.find('.sw-app-configure-link');
                configLink.on('mouseup', function () {
                    // mouseup, release the mouse button.
                    if (!PR.settings.app.find('.plugin-configure').length) {
                        // Wait the configuration page to be loaded.
                        PR.ready('.pr .plugin-configure > form', function () {
                            PR.settings.form = PR.settings.app.find('.plugin-configure > form');
                            PR.settings.load(PR.settings.form);
                        });
                    }
                });

                
                // Set events in the configuration form.

            },

            // Load the configuration form.
            load : function (f) {
                //Do nothing if the configuration form has been loaded.
                if ($('#PR').length) {
                    return;
                }

                // Create a new DOM node and insert it into the form, before the buttons.
                $('<div id="PR"></div>').insertBefore(f.find('div:last'));

                // Load the configuration options.
                plugin.renderHtmlTemplate('settings.html', {}, function (content) {
                    f = $('#PR');
                    f.html(content);

                    // Adjust blue marker height
                    $('#sw-app-row-marker').animate({height: $('.pr').height() - 5}, 250);

                    // Get the data from the plugin settings and display it in the configuration form.
                    var data = PR.settings.form.find('div.setting input[name^="data"]').val();
                    PR.data = (!data) ? [] : $.parseJSON(data);

                    /*
                     .....
                     */
                });

                // Add validation to plugin "Save" button.
                PR.settings.app.find('.sui-bttn-primary').on('mousedown', function(e) {
                    if (!PR.settings.validate()) {
                        e.stopImmediatePropagation();
                        return false;
                    }
                });
            },

            // Validate settings
            validate : function () {
                plugin.settings.data = PR.settings.app.find('div.setting input').val();

                /*
                ....
                */

                return true;
            }

        }

    };

  })(jQuery);


  SPICEWORKS.app.ready(PR.init);