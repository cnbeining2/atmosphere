define(['react', 'underscore', 'components/page_header', 'collections/applications'], function(React, _, PageHeader, Applications) {

    var ApplicationsHome = React.createClass({
        getInitialState: function() {
            return {
                applications: null
            };
        },
        helpText: function() {
            return React.DOM.p({}, "Applications are cool. You are, too. Keep bein' cool, bro.");
        },
        render: function() {
            var content = React.DOM.div({}, "loading");
            if (this.state.applications != null)
                content = React.DOM.ul({}, this.state.applications.map(function(app) {
                    return React.DOM.li({}, app.get('name')); 
                }));

            return React.DOM.div({},
                PageHeader({title: 'Applications', helpText: this.helpText}),
                content);
        },
        updateApplications: function(apps) {
            console.log(this);
            console.log(apps);
            this.setState({applications: apps});
        },
        componentDidMount: function() {
            var apps = new Applications();
            apps.on('sync', this.updateApplications);
            apps.fetch();
        },
        componentWillUnmount: function() {
            this.state.applications.off('sync', this.updateApplications);
        }
    });

    return ApplicationsHome;

});
