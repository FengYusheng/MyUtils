# Mindwalk Help Desk Candidate Fields V1

## 1. Custom Configure Page

* Supply a page to make "show" rules;
* Supply a page to make "hide" rules;

## 2. "Toggle Rules" Management
A rule is a string ending with a semicolon. All the word in the string is lowercase. The format of the rules is  "Parent, Condition 1, Condition 2, ..., Condition N, Child, show/hide;".

"Parent" and "child" are custom attributes which you edit in 'HOSTNAME/settings/helpdesk/customize-attributes' in the user portal. "Child" is shown or hidden if the parent's value is one of Condition 1, Condition 2, ... or Condition N. 

"A, 1, 2, 3, B show;" means B is shown if A's value is 1, 2, , or 3.

"A, 1, 2, ,3, B hide;" means B is hidden if A's value is 1, 2, or 3.

If a custom attribute's name exists appear in the configure page, it's hidden when we visit user portal. It will be shown until one of the custom attribute's value matches a rule.

## 3. Toggle HTML Tags In User Portal
There is a html select tag only when we visit the user portal page. When we select "Beijing Basic Request Tickets", its fields should appear in the page and the other tickets' fields should be hidden.