/**
* HELP DESK CUSTOMIZATIONS V2 - SPICEWORKS PLUGIN
* Compatible with Spiceworks 7.3 & higher (using the v2 help desk only)
* @author Brent Wong (bdewong)
* @version 0.6
* @date 2015-01-05
*/

/** CONFIGURATION PANEL SETTINGS */

plugin.configure({
  settingDefinitions:[
    {name:'past_due_color', label:'Past Due Highlight Color', type:'string', defaultValue:'#b11f1a', example:'Default: #b11f1a'},
    {name:'past_due_text', label:'Past Due Text Colro', type:'enumeration', defaultValue:'white', options:['black', 'white']},
    {name:'private_note_color', label:'Private Note Color', type:'string', defaultValue:'#eeeeee', example:'Default: #eeeeee'},
    {name:'tickets_open_display', label:'Display Open Tickets', type:'enumeration', defaultValue:'enabled', options:['enabled', 'disabled']},
    {name:'tickets_due_display', label:'Display Past Due Tickets', type:'enumeration', defaultValue:'enabled', options:['enabled', 'disabled']},
    {name:'tickets_unassigned_display', label:'Display Unassigned Tickets', type:'enumeration', defaultValue:'enabled', options:['enabled', 'disabled']},
    {name:'tickets_my_display', label:'Display My Assigned Tickets', type:'enumeration', defaultValue:'disabled', options:['enabled', 'disabled']},
    {name:'area', label:'Area to Colorize', type:'enumeration', defaultValue:'Entire Row', options:['Entire Row', 'Priority Cell']},
    {name:'priority_low_color', label:'Priority Low Color', type:'string', defaultValue:'#c9dcc8', example:'Default: #c9dcc8'},
    {name:'priority_med_color', label:'Priority Medium Color', type:'string', defaultValue:'#ffffd7', example:'Default: #ffffd7'},
    {name:'priority_high_color', label:'Priority High Color', type:'string', defaultValue:'#fc939c', example:'Default: #fc939c'},
    {name:'priority_low_text', label:'Priority Low Text Color', type:'enumeration', defaultValue:'black', options:['black', 'white']},
    {name:'priority_med_text', label:'Priority Medium Text Color', type:'enumeration', defaultValue: 'black', options:['black', 'white']},
    {name:'priority_high_text', label:'Priority High Text Color', type:'enumeration', defaultValue:'black', options:['black', 'white']}
  ]
});

SPICEWORKS.utils.addStyle(".sui-opt-in .helpdesk-app .ticket-grid .table-body .ticket-table-wrapper tr:hover td.filter-priority-low, .sui-opt-in .helpdesk-app .ticket-grid .table-body .ticket-table-wrapper tr td.filter-priority-low,.sui-opt-in .helpdesk-app .ticket-grid .table-body .ticket-table-wrapper tr.filter-priority-low:not(.selected){background-color:" + plugin.settings.priority_low_color + ";color:" + plugin.settings.priority_low_text + ";}");
SPICEWORKS.utils.addStyle(".sui-opt-in .helpdesk-app .ticket-grid .table-body .ticket-table-wrapper tr:hover td.filter-priority-med, .sui-opt-in .helpdesk-app .ticket-grid .table-body .ticket-table-wrapper tr td.filter-priority-med,.sui-opt-in .helpdesk-app .ticket-grid .table-body .ticket-table-wrapper tr.filter-priority-med:not(.selected){background-color:" + plugin.settings.priority_med_color + ";color:" + plugin.settings.priority_med_text + ";}");
SPICEWORKS.utils.addStyle(".sui-opt-in .helpdesk-app .ticket-grid .table-body .ticket-table-wrapper tr:hover td.filter-priority-high, .sui-opt-in .helpdesk-app .ticket-grid .table-body .ticket-table-wrapper tr td.filter-priority-high,.sui-opt-in .helpdesk-app .ticket-grid .table-body .ticket-table-wrapper tr.filter-priority-high:not(.selected){background-color:" + plugin.settings.priority_high_color + ";color:" + plugin.settings.priority_high_text + ";}");
SPICEWORKS.utils.addStyle(".sui-opt-in .helpdesk-app .ticket-grid .table-body .ticket-table-wrapper tr:hover td.column-due.past-due, .sui-opt-in .helpdesk-app .ticket-grid .table-body .ticket-table-wrapper tr td.column-due.past-due{background-color:" + plugin.settings.past_due_color + ";color:" + plugin.settings.past_due_text + ";}");
SPICEWORKS.utils.addStyle(".sui-opt-in .helpdesk-app .ticket-pane .tab-sections .activity.tab-pane .activity-feed .activity-event.note .activity-item{background-color:" + plugin.settings.private_note_color + ";}");

plugin.includeStyles();


/** OPTION: Ticket Counts **/
function updateTickets() {
  var strToolbar = '.page-header > .sui-bttn-toolbar';
  var strTTI = '#toolbar_ticket_info';

  if (plugin.settings.tickets_open_display=='enabled' || plugin.settings.tickets_due_display=='enabled' || plugin.settings.tickets_unassigned_display=='enabled' || plugin.settings.tickets_my_display=='enabled') {

    var grps = Array();
    if (plugin.settings.tickets_open_display=='enabled') { grps.push(["Open", "open", "open_tickets", "hdc_ticket_open_cnt"]); }
    if (plugin.settings.tickets_due_display=='enabled') { grps.push(["Past Due", "past_due", "past_due_tickets", "hdc_ticket_past_due_cnt"]); }
    if (plugin.settings.tickets_unassigned_display=='enabled') { grps.push(["Unassigned", "unassigned", "unassigned_tickets", "hdc_ticket_unassigned_cnt"]); }
    if (plugin.settings.tickets_my_display=='enabled') { grps.push(["My Tickets", "open_and_assigned_to_current_user", "my_tickets", "hdc_ticket_my_cnt"]); }

    var tti = jQuery(strTTI);
    if (tti.length === 0) {
      jQuery(strToolbar).after(jQuery('<span>').attr('id', 'toolbar_ticket_info'));
      var tti2 = jQuery(strTTI);
    }

    // Show ticket counts
    jQuery.each(grps, function() {
      var label = this[0], filter = this[1], href = this[2], id = this[3];

      // First time the ticket bar needs to be setup
      if (tti.length === 0) {
        tti2.append(
          jQuery('<a>')
            .addClass('ticket-view')
            .attr('href', '#' + href)
            .attr('data-view', href)
            .text(label + ':')
        );
        tti2.append('<span id="' + id + '"></span>');
      }

      jQuery.getJSON('/api/tickets.json?total_count=true&filter=' + filter, function(msg) {
        jQuery('#'+id).text(msg.count);
      });
    });
  }
}

/** Colorize Helpdesk **/
function Colorize() {
  jQuery('td.column-priority').each(function(){
    var p = jQuery(this);
    if (plugin.settings.area=='Entire Row') { p = p.parent(); }
    switch(jQuery.trim(jQuery(this).text())) {
      case 'High':
        p.removeClass('filter-priority-low filter-priority-med').addClass('filter-priority-high');
        break;
      case 'Med':
        p.removeClass('filter-priority-low filter-priority-high').addClass('filter-priority-med');
        break;
      case 'Low':
        p.removeClass('filter-priority-med filter-priority-high').addClass('filter-priority-low');
        break;
    }
  });

  /** The past due checking as the DOM doesn't indicate when a ticket is past due except with a flag icon **/
  jQuery('td.column-status i.icon-flag').each(function(){
    jQuery(this).parent().parent().children('td.column-due').addClass('past-due');
  });
}

function infoItem(title, data) {
  return '<li><strong>' + title + ':</strong> ' + data + '</li>';
}

function relatedItems() {

  var ticketid;

  jQuery('section.related-items').find('a.inventory-item-link').each(function(){

    var url = jQuery(this).attr('href');
    if (url.indexOf('inventory/groups') > -1) {
      var iteminfo = url.split('inventory/groups/')[1];
      var type = iteminfo.split('/')[0];
      var id = iteminfo.split('/')[1];

      var d;
      var info = '<ul>';
      if (type == 'software') {
        d = SPICEWORKS.data.Software.find(id);
        if (d.vendor && !d.vendor.empty()) { info += infoItem('Vendor', d.vendor); }
        if (d.url_info_about && !d.url_info_about.empty()) { info += infoItem('URL', d.url_info_about); }
        if (d.licenses) { info += infoItem('Licenses', d.licenses); }
        if (d.install_date && !d.install_date.empty()) { info += infoItem('Installed', d.install_date); }
        if (d.open_ticket_count) { info += infoItem('Open Tickets', d.open_ticket_count); }
        if (d.software_installations_count) { info += infoItem('Installations', d.software_installations_count); }
        if (d.error_alert_count) { info += infoItem('Errors', d.error_alert_count); }
        if (d.warning_alert_count) { info += infoItem('Warnings', d.warning_alert_count); }
      } else if (type == 'devices') {
        d = SPICEWORKS.data.Device.find(id);
        if (d.ip_address && !d.ip_address.empty()) { info += infoItem('IP', d.ip_address); }
        if (d.mac_address && !d.mac_address.empty()) { info += infoItem('MAC', d.mac_address); }
        if (d.manufacturer && !d.manufacturer.empty()) { info += infoItem('Vendor', d.manufacturer); }
        if (d.current_user && !d.current_user.empty()) { info += infoItem('Last Login', d.current_user); }
        if (d.primary_owner_name && !d.primary_owner_name.empty()) { info += infoItem('Owner', d.primary_owner_name); }
        if (d.asset_tag && !d.asset_tag.empty()) { info += infoItem('Asset Tag', d.asset_tag); }
        if (d.operating_system && !d.operating_system.empty()) { info += infoItem('OS', d.operating_system); }
        if (d.serial_number && !d.serial_number.empty()) { info += infoItem('Serial No', d.serial_number); }
      }

      if (info.length > 4) {
        info += '</ul>';

        var poptitle = jQuery(this).find('p.title').text();

        jQuery(this).find('.card').append(jQuery('<a>')
          .addClass('related-item-info')
          .attr('id', 'related-popover-' + id)
          .append(jQuery('<i>')
            .addClass('icon-search icon-blue')
          )
          .css({
            'cursor': 'pointer',
            'position': 'absolute',
            'top' : '4px',
            'left' : '6px'
          })
          .popover({
            placement: 'right',
            trigger: 'click',
            title: poptitle,
            content: info,
            container: '#tabs_14-related'
          })
        );
      }
    }
  });
}

function updateBoth(){
  Colorize();
  updateTickets();
}

/* Helpdesk loaded */
$UI.app.pluginEventBus.on('app:primary:show', function(){
  updateBoth();
});

/* Ticket loaded */
$UI.app.pluginEventBus.on('app:secondary:show', function(){
  Colorize();
  relatedItems();
});

$UI.app.pluginEventBus.on('app:helpdesk:ticket:change:status', function(ticket){
  if (ticket.status=='closed') {
    setTimeout(updateBoth, 5000);
  }
});

$UI.app.pluginEventBus.on('app:helpdesk:ticket:add', function(){
  setTimeout(updateBoth, 5000);
  /*alert('app:helpdesk:ticket:add');
  setTimeoutColorize();
  updateTickets();*/
});

/*
jQuery(document).ajaxSend(function(e,x,s) {
  console.log('ajaxSend: ' + s.url);
});
HelpDesk.vent.on('view:changed', function() {
  alert("Helpdesk.vent.on('view:changed')");
});
HelpDesk.vent.on('ticket:changed', function() {
  alert("Helpdesk.vent.on('ticket:changed')");
});
HelpDesk.vent.on('comment:added', function() {
  alert("Helpdesk.vent.on('comment:added')");  
});
*/