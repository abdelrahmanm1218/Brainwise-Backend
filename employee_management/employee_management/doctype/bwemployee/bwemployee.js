// Copyright (c) 2025, mw and contributors
// For license information, please see license.txt


frappe.ui.form.on('BWEmployee', {

    refresh: function(frm) {
        // Filter Departments by Company
        frm.set_query("department", function() {
            if (!frm.doc.company) {
                return {
                    filters: {
                        name: ["is", "set"]
                    }
                };
            }

            return {
                filters: {
                    company: frm.doc.company
                }
            };
        });

        // Calculate days on form load for accuracy
        if (frm.doc.hired_on) {
            calculate_days_with_company(frm);
        }
    },

    hired_on: function(frm) {
        // Calculate days whenever hiring date changes
        if (frm.doc.hired_on) {
            calculate_days_with_company(frm);
        }
    }
});

// Helper function
function calculate_days_with_company(frm) {
    const today = new Date();
    const hireDate = new Date(frm.doc.hired_on);

    const diffTime = today - hireDate;
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

    frm.set_value("days_employeed", diffDays);
}


// frappe.ui.form.on('BWEmployee', {
//     refresh: function(frm) {
//         frm.set_query("department", function() {
//             if (!frm.doc.company) {
//                 return {
//                     filters: {
//                         name: ["is", "set"]  // return nothing unless company is selected
//                     }
//                 };
//             }

//             return {
//                 filters: {
//                     company: frm.doc.company
//                 }
//             };
//         });
//     }
// });

// frappe.ui.form.on("BWEmployee", {
// 	refresh(frm) {

// 	},
// });
