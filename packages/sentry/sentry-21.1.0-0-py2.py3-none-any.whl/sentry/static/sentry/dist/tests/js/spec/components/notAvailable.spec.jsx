import React from 'react';
import { mountWithTheme } from 'sentry-test/enzyme';
import NotAvailable from 'app/components/notAvailable';
describe('NotAvailable', function () {
    it('renders', function () {
        var wrapper = mountWithTheme(<NotAvailable />);
        expect(wrapper.text()).toEqual('\u2014');
    });
});
//# sourceMappingURL=notAvailable.spec.jsx.map