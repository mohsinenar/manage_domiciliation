odoo.define('manage.dashboard', function (require) {
    "use strict";
    var AbstractAction = require('web.AbstractAction');
    var web_client = require('web.web_client');
    var FieldRegistry = require('web.field_registry');
    var core = require('web.core');
    var _t = core._t;
    var rpc = require('web.rpc');
    var session = require('web.session');
    var QWeb = core.qweb;

    var my_dashboard = AbstractAction.extend({
        template: 'manage.HrdashboardMain',
        events: {
            'click .add_client': 'addClient',
            'click .add_company': 'addCompany',
            'click .list_client': 'listClients',
            'click .list_companies': 'listCompanies',
        },
        init: function (parent, context) {
            this._super(parent, context);
            this.clients = [];
            this.companies = [];
        },
        addClient(e) {
            var options = {}
            this.do_action({
                name: _t("Clients"),
                type: 'ir.actions.act_window',
                res_model: 'manage.client',
                res_id: false,
                view_mode: 'tree,form',
                views: [[false, 'form']],
                target: 'current'
            }, options)
        },
        addCompany(e) {
            var options = {}
            this.do_action({
                name: _t("Companies--"),
                type: 'ir.actions.act_window',
                res_model: 'manage.company',
                res_id: false,
                view_mode: 'tree,form',
                views: [[false, 'form']],
                target: 'current'
            }, options)
        },
        listClients(e) {
            var options = {}
            this.do_action({
                name: _t("Clients"),
                type: 'ir.actions.act_window',
                res_model: 'manage.client',
                view_mode: 'tree,form',
                views: [[false, 'list'], [false, 'form']],
                target: 'current'
            }, options)
        },
        listCompanies(e) {
            var options = {}
            this.do_action({
                name: _t("Companies --"),
                type: 'ir.actions.act_window',
                res_model: 'manage.company',
                view_mode: 'tree,form',
                views: [[false, 'list'], [false, 'form']],
                target: 'current'
            }, options)
        },
        start: function () {
            var self = this;
            this.set("title", 'dashboard');
            return this._super().then(function () {
                self.render_dashboards();
                self.$el.parent().addClass('oe_background_grey');
            });
        },
        willStart: function () {
            var self = this;
            return self.fetch_data();
        },
        fetch_data: function () {
            var self = this;
            var def0 = self._rpc({
                model: 'manage.client',
                method: 'search_read'
            }).then(function (result) {
                self.clients = result;
            });

            var def1 = self._rpc({
                model: 'manage.company',
                method: 'search_read',
                domain: [
                    ['status', '=', 'close_to_end']
                ]
            }).then(function (result) {
                console.log(result)
                self.companies = result;
            });
            return $.when(def0, def1);
        },
        render_dashboards: function () {
            var self = this;
            // self.$('.Clients').append(QWeb.render('Clientsdashboard', { widget: self }));
            self.$('.Companies').append(QWeb.render('CompaniesDashboard', { widget: self }));
        },

    });
    core.action_registry.add('my_dashboard', my_dashboard);
    return my_dashboard;

})