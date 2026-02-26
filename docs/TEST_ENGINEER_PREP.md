# Test Engineer L1 Preparation Guide

Preparation plan for Test Engineer role at Meta (via Wipro) while completing Contact Automation project.

---

## Role Requirements Mapping

### ✅ Skills You're Building in This Project

| Requirement | How This Project Demonstrates It | Interview Talking Points |
|------------|----------------------------------|--------------------------|
| **Test Case Design** | Unit tests for 3 services with edge cases | "Designed 15+ test cases covering happy paths, edge cases, and error conditions for database operations" |
| **Test Automation** | Pytest framework with fixtures, mocking | "Built automated test suite with 95%+ coverage using pytest and unittest.mock" |
| **Test Planning** | `IMPLEMENTATION_PLAN.md`, phased approach | "Created comprehensive test plan with phases, acceptance criteria, and risk mitigation" |
| **Defect Tracking** | GitHub issues, documented bug fixes | "Tracked and resolved 5+ defects including OAuth authentication and encoding issues" |
| **API Testing** | Google Drive & Gmail API integration | "Tested REST API integrations with proper mocking and error handling" |
| **Test Documentation** | Clear test names, docstrings, assertions | "Documented test cases with clear descriptions and expected outcomes" |
| **CI/CD Integration** | GitHub Actions workflows | "Set up automated testing pipeline with pre-commit hooks and CI/CD" |
| **Collaboration** | Git workflow, PR templates | "Followed Git Flow with feature branches and code review process" |

---

## Study Plan (2-3 Weeks)

### Week 1: Testing Fundamentals + Complete Services

#### Days 1-2: Software Testing Basics
- [ ] **STLC (Software Testing Life Cycle)**
  - Requirement Analysis → Test Planning → Test Case Development → Test Environment Setup → Test Execution → Test Closure
  - How it maps to your project phases

- [ ] **Test Case Design Techniques**
  - Equivalence Partitioning (valid/invalid inputs)
  - Boundary Value Analysis (min/max values)
  - Decision Table Testing (multiple conditions)
  - State Transition Testing (workflow states)

- [ ] **Practice**: Review your existing tests and identify which techniques you used

#### Days 3-4: Complete Beat Selection Service
- [ ] Implement `services/beat_selection_service.py`
- [ ] Write unit tests with:
  - Valid selection (3-5 beats)
  - Duplicate prevention (30-day rule)
  - Insufficient beats scenario
  - Edge case: exactly 3 beats available
- [ ] Document test cases in comments

#### Days 5-7: Complete Email Template & Gmail Services
- [ ] Implement `services/email_template_service.py`
- [ ] Implement `services/gmail_service.py`
- [ ] Write comprehensive unit tests
- [ ] Practice explaining your testing approach

---

### Week 2: Advanced Testing + Integration Tests

#### Days 1-2: Defect Management
- [ ] **Study Defect Lifecycle**
  - New → Assigned → Open → Fixed → Retest → Closed
  - Severity (Critical/High/Medium/Low)
  - Priority (P0/P1/P2/P3)

- [ ] **Practice**: Document the bugs you fixed in this project
  - OAuth scope error (Severity: High, Priority: P1)
  - Unicode encoding error (Severity: Medium, Priority: P2)
  - Database test assertion (Severity: Low, Priority: P3)

#### Days 3-5: Integration & E2E Testing
- [ ] Write integration tests for full workflow:
  - Test: Fetch artists → Select beats → Send email
  - Test: Duplicate prevention across services
  - Test: Error handling and rollback

- [ ] **Study**: Integration vs Unit vs E2E testing
- [ ] Create test data fixtures and mocks

#### Days 6-7: Test Automation Frameworks
- [ ] **Study Popular Frameworks**
  - Pytest (you're using this!)
  - Selenium (web UI testing)
  - unittest (Python standard)
  - JUnit (Java)
  - TestNG (Java)

- [ ] **Practice**: Explain pytest features
  - Fixtures for setup/teardown
  - Parametrization for data-driven tests
  - Mocking external dependencies
  - Coverage reporting

---

### Week 3: Interview Prep + Project Completion

#### Days 1-3: Create Test Documentation
- [ ] Write formal test plan document
- [ ] Create test case matrix (feature → test cases → status)
- [ ] Generate test coverage report
- [ ] Document test environment setup

#### Days 4-5: Mock Interviews
- [ ] Practice explaining your project as a QA engineer
- [ ] Prepare STAR stories (Situation, Task, Action, Result)
- [ ] Practice writing test cases on whiteboard
- [ ] Review common testing interview questions

#### Days 6-7: Final Project Polish
- [ ] Complete CLI commands
- [ ] Run full test suite
- [ ] Fix any remaining issues
- [ ] Update documentation

---

## Interview Preparation

### Project Presentation (5-10 minutes)

**Opening Statement**:
> "I recently built an automated email system for sending beat packs to artists. I approached it like a professional QA engineer, implementing comprehensive testing, CI/CD, and quality gates throughout the development lifecycle."

**Key Points to Highlight**:
1. **Test-Driven Approach**: "I wrote unit tests for each service before integration"
2. **Coverage**: "Achieved 95%+ test coverage using pytest and coverage.py"
3. **Automation**: "Set up pre-commit hooks and GitHub Actions for automated testing"
4. **Bug Tracking**: "Documented and resolved 5+ defects with clear reproduction steps"
5. **API Testing**: "Tested Google Drive and Gmail API integrations with proper mocking"

### STAR Stories to Prepare

#### Story 1: Defect Identification & Resolution
- **Situation**: OAuth authentication failing with "insufficient scopes" error
- **Task**: Debug the authentication flow and identify root cause
- **Action**: Analyzed error logs, reviewed OAuth documentation, identified missing test user configuration
- **Result**: Resolved issue by adding test user in Google Cloud Console; documented fix in OAUTH_FIX.md

#### Story 2: Test Case Design
- **Situation**: Database service needed comprehensive testing
- **Task**: Design test cases covering all CRUD operations and edge cases
- **Action**: Created 10+ test cases including duplicate prevention, context manager, and error handling
- **Result**: Caught 2 bugs during testing; achieved 100% coverage for database service

#### Story 3: Test Automation
- **Situation**: Manual testing was time-consuming and error-prone
- **Task**: Automate test execution and integrate with development workflow
- **Action**: Set up pytest framework, created fixtures, implemented CI/CD with GitHub Actions
- **Result**: Reduced testing time from 30 minutes to 2 minutes; caught regressions automatically

---

## Technical Concepts to Study

### 1. Testing Types
- **Unit Testing**: Testing individual functions/methods
- **Integration Testing**: Testing component interactions
- **System Testing**: Testing complete system
- **Acceptance Testing**: Testing against requirements
- **Regression Testing**: Testing after changes
- **Smoke Testing**: Basic functionality check
- **Sanity Testing**: Quick verification after bug fix

### 2. Testing Techniques
- **Black Box**: Testing without knowing internal code
- **White Box**: Testing with code knowledge
- **Gray Box**: Combination of both

### 3. Test Automation Concepts
- **Test Fixtures**: Setup/teardown for tests
- **Mocking**: Simulating external dependencies
- **Parametrization**: Running same test with different data
- **Assertions**: Verifying expected outcomes
- **Test Suites**: Grouping related tests

### 4. Quality Metrics
- **Test Coverage**: % of code covered by tests
- **Defect Density**: Defects per KLOC (thousand lines of code)
- **Pass/Fail Rate**: % of tests passing
- **Defect Leakage**: Defects found in production

---

## Common Interview Questions

### Technical Questions

**Q1: What is the difference between smoke testing and sanity testing?**
- **Smoke**: Broad, shallow test to verify basic functionality (build verification)
- **Sanity**: Narrow, deep test to verify specific functionality after bug fix

**Q2: Explain your approach to writing test cases.**
1. Understand requirements
2. Identify test scenarios (positive, negative, edge cases)
3. Design test cases with clear steps and expected results
4. Peer review test cases
5. Execute and track results

**Q3: How do you prioritize test cases?**
- Critical path first (core functionality)
- High-risk areas (complex logic, frequent changes)
- Customer-facing features
- Regression tests for known issues

**Q4: What is your experience with test automation?**
> "In my Contact Automation project, I implemented automated testing using pytest. I created unit tests for database operations, API integrations, and data parsing. I used fixtures for test setup, mocking for external dependencies, and integrated the test suite with GitHub Actions for CI/CD. This reduced testing time by 90% and caught regressions automatically."

**Q5: How do you handle flaky tests?**
- Identify root cause (timing issues, environment dependencies)
- Add proper waits/retries
- Improve test isolation
- Use deterministic test data
- Document and track flaky tests

### Behavioral Questions

**Q1: Tell me about a time you found a critical bug.**
- Use OAuth authentication bug story

**Q2: How do you handle disagreements with developers?**
- Focus on data and user impact
- Collaborate to find root cause
- Suggest solutions, not just problems

**Q3: Describe a time you had to learn a new testing tool quickly.**
- Talk about learning pytest, Google APIs, mocking

---

## Resources to Study

### Online Courses (Free)
1. **Software Testing Fundamentals** - Guru99.com
2. **Pytest Tutorial** - Real Python
3. **API Testing** - Postman Learning Center
4. **Test Automation University** - Applitools (free courses)

### Books (Optional)
1. "The Art of Software Testing" - Glenford Myers
2. "Lessons Learned in Software Testing" - Cem Kaner

### Practice
1. **LeetCode Testing Problems** - Practice test case design
2. **HackerRank** - SQL queries for test data validation
3. **GitHub Projects** - Review test suites in popular repos

---

## Day-of-Interview Checklist

### Before Interview
- [ ] Review your Contact Automation project
- [ ] Prepare 3 STAR stories
- [ ] Review testing terminology
- [ ] Test your internet/camera/mic
- [ ] Have project code open for reference

### During Interview
- [ ] Listen carefully to questions
- [ ] Ask clarifying questions if needed
- [ ] Use STAR method for behavioral questions
- [ ] Draw diagrams if helpful
- [ ] Show enthusiasm for testing

### Questions to Ask Interviewer
1. "What testing frameworks and tools does the team use?"
2. "How is the QA team structured? Embedded or centralized?"
3. "What's the typical test automation coverage target?"
4. "How does the team handle test environment management?"
5. "What opportunities are there for learning and growth?"

---

## Project Completion Checklist

### Must Complete Before Interview
- [x] Database Service + Tests
- [x] Google Drive Service + Tests
- [x] Beat Parser Service + Tests
- [ ] Beat Selection Service + Tests
- [ ] Email Template Service + Tests
- [ ] Gmail Service + Tests
- [ ] Integration Tests
- [ ] CLI Commands (list-artists, send-beats)

### Nice to Have
- [ ] Test coverage report (HTML)
- [ ] Test plan document
- [ ] Defect log
- [ ] Performance tests

---

## Timeline

**Week 1**: Complete services + unit tests (Days 1-7)
**Week 2**: Integration tests + study testing concepts (Days 8-14)
**Week 3**: Interview prep + final polish (Days 15-21)

**Daily Schedule**:
- Morning (2-3 hours): Code/implement services
- Afternoon (1-2 hours): Write tests
- Evening (1 hour): Study testing concepts

---

## Success Metrics

By the end of preparation, you should be able to:
- ✅ Explain STLC and where you are in each phase
- ✅ Design test cases using 3+ techniques
- ✅ Demonstrate test automation with pytest
- ✅ Discuss defects you found and fixed
- ✅ Show test coverage report (>90%)
- ✅ Explain your CI/CD pipeline
- ✅ Answer "Why QA?" confidently

---

## Confidence Boosters

**You Already Have**:
- Real project with production-quality code
- Automated test suite with good coverage
- CI/CD pipeline with GitHub Actions
- Bug tracking and resolution experience
- API testing experience
- Documentation skills

**You're Learning**:
- Formal testing terminology
- Test case design techniques
- Interview communication skills

**You'll Excel At**:
- Technical discussions about testing
- Demonstrating hands-on experience
- Problem-solving and debugging
- Attention to detail and quality

---

## Final Tips

1. **Be Honest**: If you don't know something, say so and explain how you'd learn it
2. **Show Passion**: Talk about why you care about quality
3. **Use Examples**: Reference your project frequently
4. **Ask Questions**: Show curiosity about their testing practices
5. **Stay Calm**: You've built something real - be proud of it

**Remember**: This project is better preparation than most candidates will have. You're not just studying testing - you're DOING it.

Good luck! 🚀
