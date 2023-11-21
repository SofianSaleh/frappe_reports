// Copyright (c) 2023, a and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Test Reports"] = {
  onload: function () {
    frappe.query_report._get_filters_html_for_print =
      frappe.query_report.get_filters_html_for_print;
    frappe.query_report.get_filters_html_for_print = (print_settings) => {
      const me = frappe.query_report,
        encode = (svg) =>
          "data:image/svg+xml;base64," +
          btoa(new XMLSerializer().serializeToString(svg));
      let applied_filters = me._get_filters_html_for_print();
      console.log(me);
      if (me.raw_data && me.raw_data.message.length > 0) {
        applied_filters += `<hr><h3>${me.raw_data.message}</h3></hr>`;
      }

      if (me.raw_data.report_summary && me.raw_data.report_summary.length > 0) {
        var rs = me.raw_data.report_summary;

        applied_filters += `<div class="report-summary" style="background-color: var(--bg-color);
        border-radius: var(--border-radius-md, 8px);
        border-bottom: 1px solid var(--border-color);
        margin: 1rem;
        padding: 20px 15px;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-evenly;
        gap: 20px;">`;
        for (var i = 0; i < rs.length; i++) {
          applied_filters += `
          <div class="summary-item" 
          style="margin: 0px 20px;
          min-width: 160px;
          max-width: 300px;
          height: 62px;
          display: flex;
          flex-direction: column;
          place-content: center;"
          >\n\t\t\t

          <span class="summary-label" style="ont-size: var(--text-base);
          font-weight: normal !important;
          text-align: center;
          overflow: hidden !important;
          text-overflow: ellipsis;
          white-space: nowrap;">${rs[i].label}</span>
          \n\t\t\t

          <div class="summary-value " 
          style="font-size: var(--text-2xl, 20px);
          font-weight: 600;
          line-height: 16px;
          color: var(--text-color);
          font-feature-settings: 'tnum';
          padding-top: 12px;
          padding-bottom: 5px;
          text-align: center;
          overflow: hidden !important;
          text-overflow: ellipsis;
          white-space: nowrap;"
          >${rs[i].value}</div>
          \n\t\t
          </div>
			`;
        }
        applied_filters += `</div>`;
      }

      if (me.chart && me.chart.svg) {
        applied_filters += `<hr><img alt="${__("Chart")}" src="${encode(
          me.chart.svg
        )}" />`;
      }

      return applied_filters;
    };
  },
  filters: [
    {
      fieldname: "item_group",
      label: "Item Group",
      fieldtype: "Link",
      options: "Item Group",
    },
    {
      fieldname: "name",
      label: "Name",
      fieldtype: "Link",
      options: "Item",
    },
    {
      fieldname: "is_wooet_product",
      label: "Is Woocommerce Product",
      fieldtype: "Check",
      options: "Item",
    },
    {
      fieldname: "woocommerce_id",
      label: "Woocommerce ID",
      fieldtype: "Data",
      options: "Item",
    },
  ],
};
