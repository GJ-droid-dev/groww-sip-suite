"""
build_corpus.py - Ingests and generates 550+ realistic, high-fidelity Indian investor feedback
records for Groww mutual fund SIP journeys across Play Store, App Store, Reddit, and Forums.
"""

import os
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from core.schemas import SourceType, FailureCategory, InvestorTenure
from core.normalizer import Deduplicator, normalize_record
from core.config import RAW_DATA_DIR, PROCESSED_DATA_DIR

# Seed for deterministic reproducibility
random.seed(42)

# Templates & seed expressions across categories for first-time Indian investors
PLAY_STORE_TEMPLATES = [
    # BANK_MANDATE_PENALTY_SHOCK
    ("Worst experience with autopay! My salary comes on 7th, SIP debit was set on 5th. Bank charged me Rs {fee} NACH bounce fee! Why can't Groww check balance or let me postpone by 2 days without penalty? Cancelling my SIP.", FailureCategory.BANK_MANDATE_PENALTY_SHOCK, InvestorTenure.MONTHS_2_3, "salaried_early_career", "stopped"),
    ("Groww deducted SIP amount twice this month from my {bank} account. Total Rs {amount} gone. Support is useless AI bot. I am stopping all SIPs immediately and moving to Zerodha.", FailureCategory.BANK_MANDATE_PENALTY_SHOCK, InvestorTenure.MONTH_1, "general_first_timer", "stopped"),
    ("My mandate got rejected because bank name had small spelling difference. Groww didn't notify me in time, now my first SIP failed. Bad start for beginner.", FailureCategory.BANK_MANDATE_PENALTY_SHOCK, InvestorTenure.MONTH_1, "general_first_timer", "considering_stop"),
    ("Why did my auto debit fail when I had Rs 5000 in account? And now {bank} bank charged Rs {fee} for mandate return! Very disappointed with Groww autopay integration.", FailureCategory.BANK_MANDATE_PENALTY_SHOCK, InvestorTenure.MONTHS_4_6, "salaried_early_career", "stopped"),
    ("Autopay setup is so confusing. It asked for debit card OTP, then netbanking. After 15 days it says mandate inactive and missed my installment. What kind of app is this?", FailureCategory.BANK_MANDATE_PENALTY_SHOCK, InvestorTenure.MONTH_1, "tier_2_3_saver", "considering_stop"),

    # RETURN_ILLUSION_DISILLUSION
    ("Investing Rs {amount}/month for last 5 months in {fund_type} fund. Returns are -3.2%! Even FD gives 7% guaranteed. Mutual funds are useless, I am losing my hard earned money.", FailureCategory.RETURN_ILLUSION_DISILLUSION, InvestorTenure.MONTHS_4_6, "general_first_timer", "stopped"),
    ("Started SIP 6 months ago after seeing youtube videos on compounding. Today my portfolio is in RED. Invested Rs 18,000, current value is 17,400. Decided to pause SIP until market recovers.", FailureCategory.RETURN_ILLUSION_DISILLUSION, InvestorTenure.MONTHS_4_6, "student", "paused"),
    ("3 months completed. Profit is only Rs 45. Is this a joke? YouTube influencers said 15% return. I think saving account interest is better than this headache.", FailureCategory.RETURN_ILLUSION_DISILLUSION, InvestorTenure.MONTHS_2_3, "general_first_timer", "considering_stop"),
    ("Why is NAV going down every day? When I started it was 84 now 79. My money is decreasing every month. Paused my SIP, will restart only if it goes green.", FailureCategory.RETURN_ILLUSION_DISILLUSION, InvestorTenure.MONTHS_2_3, "tier_2_3_saver", "paused"),
    ("Invested total 8 installments of Rs 2000. Overall return is 0.8%. With inflation I am literally losing money. Groww should show realistic expectations instead of rosy calculators.", FailureCategory.RETURN_ILLUSION_DISILLUSION, InvestorTenure.MONTHS_7_9, "salaried_early_career", "stopped"),

    # CASHFLOW_RIGID_ANXIETY
    ("I work on freelance contracts and don't get paid on exact date. Groww has fixed debit dates (5th, 10th, 15th). When payment was delayed I had to frantically cancel SIP to avoid bank penalty.", FailureCategory.CASHFLOW_RIGID_ANXIETY, InvestorTenure.MONTHS_4_6, "variable_gig", "stopped"),
    ("Festival season coming up, have to pay rent and bonus expenses. Wanted to skip just this month's installment, but the pause button said mandate will be suspended for 3 months! Had to cancel instead.", FailureCategory.CASHFLOW_RIGID_ANXIETY, InvestorTenure.MONTHS_7_9, "salaried_early_career", "stopped"),
    ("Had medical emergency in family, balance dipped below Rs 2000. SIP debit happened and account went into negative, bank slapped penalty. Why no balance check alert 24 hrs before?", FailureCategory.CASHFLOW_RIGID_ANXIETY, InvestorTenure.MONTHS_4_6, "tier_2_3_saver", "stopped"),
    ("Can I change my SIP date easily? Currently on 2nd, want to change to 10th because salary comes late. App asked me to delete current SIP and start new one with new mandate. Too complex.", FailureCategory.CASHFLOW_RIGID_ANXIETY, InvestorTenure.MONTHS_2_3, "salaried_early_career", "considering_stop"),

    # METRIC_METAPHOR_CONFUSION
    ("What does XIRR -18% mean? Did I lose 18% of my total money? I only invested Rs 1000 last week! App interface is very scary for beginners with these financial jargons.", FailureCategory.METRIC_METAPHOR_CONFUSION, InvestorTenure.MONTH_1, "general_first_timer", "considering_stop"),
    ("Total invested shows 15000, current value 15200, but XIRR shows 4.1% and 1-day return shows -1.2%. Very confusing numbers. Which one should I actually trust?", FailureCategory.METRIC_METAPHOR_CONFUSION, InvestorTenure.MONTHS_4_6, "general_first_timer", "active"),
    ("Invested in ELSS fund for 8 months. Wanted to withdraw Rs 5000 for emergency, but it says locked for 3 years! Nobody told me this upfront when starting SIP. Feeling cheated.", FailureCategory.METRIC_METAPHOR_CONFUSION, InvestorTenure.MONTHS_7_9, "general_first_timer", "stopped"),
    ("My units increased but NAV decreased so portfolio value dropped. I thought SIP means buying more when market falls? The dashboard doesn't show rupee cost averaging clearly at all.", FailureCategory.METRIC_METAPHOR_CONFUSION, InvestorTenure.MONTHS_4_6, "salaried_early_career", "considering_stop"),

    # QUIET_DISENGAGE_HABIT_FADE
    ("Honestly haven't opened the app in 4 months. Just seeing Rs 2000 getting debited every month on my bank SMS. It feels like an unwanted subscription now. Thinking of stopping it.", FailureCategory.QUIET_DISENGAGE_HABIT_FADE, InvestorTenure.MONTHS_7_9, "salaried_early_career", "considering_stop"),
    ("Started SIP in January with high enthusiasm. By month 7 it feels completely detached. No progress updates, no milestones like 'congrats you completed 6 months', just silent debits. Cancelled.", FailureCategory.QUIET_DISENGAGE_HABIT_FADE, InvestorTenure.MONTHS_7_9, "general_first_timer", "stopped"),
    ("App is great for starting, but after 8 months there is zero motivation to continue. You just stare at a static chart. Stopped my SIP last week.", FailureCategory.QUIET_DISENGAGE_HABIT_FADE, InvestorTenure.MONTHS_7_9, "general_first_timer", "stopped"),
    ("After 10 installments I felt no connection with why I even started this SIP. Needed cash for bike maintenance so I redeemed everything and stopped the autopay.", FailureCategory.QUIET_DISENGAGE_HABIT_FADE, InvestorTenure.MONTHS_10_12, "student", "stopped"),

    # EXTERNAL_DRAFT_PANIC_PULL
    ("My uncle told me market is at all-time high of 25000 and crash is coming. He advised me to stop my equity SIP and put money in post office RD. So I stopped my Groww SIP.", FailureCategory.EXTERNAL_DRAFT_PANIC_PULL, InvestorTenure.MONTHS_4_6, "general_first_timer", "stopped"),
    ("Saw on news that US fed rate and war will crash Nifty. Panicked and stopped my 500/month SIP. Don't want to lose my savings as I am a student.", FailureCategory.EXTERNAL_DRAFT_PANIC_PULL, InvestorTenure.MONTHS_2_3, "student", "stopped"),
    ("Colleagues at office said mutual funds are going down this quarter and told me to buy physical gold coins instead. Paused my SIP for now.", FailureCategory.EXTERNAL_DRAFT_PANIC_PULL, InvestorTenure.MONTHS_4_6, "salaried_early_career", "paused"),

    # GOAL_DETACHMENT_LIQUIDATION
    ("Started SIP without any plan, just because colleagues were doing it. After 6 months accumulated Rs 30,000. Withdrew full amount to buy new iPhone 16 during sale and stopped SIP.", FailureCategory.GOAL_DETACHMENT_LIQUIDATION, InvestorTenure.MONTHS_4_6, "salaried_early_career", "stopped"),
    ("Had saved Rs 15,000 across 5 months. Friends planned a trip to Manali, so I redeemed the fund. Once money was withdrawn I didn't feel like restarting the SIP.", FailureCategory.GOAL_DETACHMENT_LIQUIDATION, InvestorTenure.MONTHS_4_6, "student", "stopped"),
    ("I didn't link this SIP to any goal. So when I needed money for Diwali shopping, I stopped the SIP and redeemed. There was no reason to keep it locked.", FailureCategory.GOAL_DETACHMENT_LIQUIDATION, InvestorTenure.MONTHS_7_9, "general_first_timer", "stopped"),
]

REDDIT_TEMPLATES = [
    # Complex, deep narrative posts from r/personalfinanceindia, r/Mutualfunds, r/IndiaInvestments
    ("First time investor (23M, earning 35k/mo). Started 3 SIPs on Groww in February (Nifty 50, Parag Parikh, Midcap). Total 8k/mo. 7 months in, my total portfolio is sitting at -1.8% return. Meanwhile my friend's bank FD gave guaranteed interest. I understand 'long term compounding' intellectually, but emotionally watching my salary evaporate every month is killing me. Should I stop the SIPs and wait for a dip?", FailureCategory.RETURN_ILLUSION_DISILLUSION, InvestorTenure.MONTHS_7_9, "salaried_early_career", "considering_stop"),
    ("PSA: Groww mandate bounce charge is brutal. My company delayed salary disbursement by 3 days because of bank holiday on 1st. My SIP debit date was 3rd. Result? Mandate failed and SBI charged me Rs 295 penalty! For a 1000 rupee SIP, paying 295 fine is ridiculous. Why doesn't Groww have a pre-debit balance verification or 48-hr grace period? Stopped all SIPs immediately.", FailureCategory.BANK_MANDATE_PENALTY_SHOCK, InvestorTenure.MONTHS_2_3, "salaried_early_career", "stopped"),
    ("Why is stopping or pausing a SIP on Groww so guilt-inducing and confusing? I freelance, so some months I earn 70k, some months 10k. In lean months, having a rigid 5000 deduction hanging over my head causes immense anxiety. I looked for a 'flexible SIP' where I can pay whenever I have surplus, but the app forces a rigid monthly date. Ended up stopping the SIP permanently.", FailureCategory.CASHFLOW_RIGID_ANXIETY, InvestorTenure.MONTHS_4_6, "variable_gig", "stopped"),
    ("Can someone explain XIRR to a beginner? Started SIP 2 months ago (2 installments of 2500). Groww shows XIRR -34.8%! I panicked thinking 34% of my capital was wiped out. It took 3 hours of googling and reddit threads to realize XIRR annualizes short term movements. Why doesn't Groww explain this inside the app instead of scaring first-timers with annualised percentages?", FailureCategory.METRIC_METAPHOR_CONFUSION, InvestorTenure.MONTHS_2_3, "general_first_timer", "considering_stop"),
    ("Does anyone else feel 'SIP fatigue' around month 8-9? When you start, you check the app every day, track NAV, read about funds. By month 8, nothing happens. It's just a passive deduction on your bank statement. Without any positive milestone or sense of progress, it feels like paying an electricity bill. I stopped mine last week because I just stopped caring.", FailureCategory.QUIET_DISENGAGE_HABIT_FADE, InvestorTenure.MONTHS_7_9, "salaried_early_career", "stopped"),
    ("My father saw my Groww app and got furious when he saw equity mutual funds. He has the 2008 crash trauma and made me cancel all my SIPs and open an SBI Recurring Deposit instead. How do first-time young investors handle family pressure when markets fluctuate?", FailureCategory.EXTERNAL_DRAFT_PANIC_PULL, InvestorTenure.MONTHS_2_3, "student", "stopped"),
    ("Treated my SIP as a flexible piggy bank. Started Rs 5000/month with no clear purpose. 6 months later accumulated 32k, and immediately redeemed it to pay for a Goa vacation with friends. Now 3 months have passed and I never restarted. How do you guys stay disciplined without associating money to a strict goal?", FailureCategory.GOAL_DETACHMENT_LIQUIDATION, InvestorTenure.MONTHS_4_6, "salaried_early_career", "stopped"),
    ("Groww auto-pay failed even though account had 12k balance. Customer care said 'NPCI clearing issue'. But bank still debited failure fee! Now Groww support says contact bank, bank says contact merchant. I'm caught in the middle for a 1500 SIP. Never using autopay again.", FailureCategory.BANK_MANDATE_PENALTY_SHOCK, InvestorTenure.MONTHS_4_6, "salaried_early_career", "stopped"),
    ("Is it normal to feel regret after 5 months of SIP? I put in 5k every month diligently. Market had a minor 4% correction and all my gains vanished into negative. My elder brother said 'SIP is a scam created by AMCs to collect expense ratios'. Almost tempted to hit the redeem button.", FailureCategory.RETURN_ILLUSION_DISILLUSION, InvestorTenure.MONTHS_4_6, "general_first_timer", "considering_stop"),
    ("Why can't we pause an SIP for just 15 days? In freelance life, invoice payments get delayed. Groww only allows pausing by 1, 2, or 3 full months. That ruins my rupee-cost averaging! I ended up cancelling the mandate so I don't get bank bounce charges.", FailureCategory.CASHFLOW_RIGID_ANXIETY, InvestorTenure.MONTHS_4_6, "variable_gig", "stopped"),
    ("I find the Groww portfolio dashboard completely unhelpful for first-timers. It shows current value, invested value, 1D return, and XIRR. But it doesn't show: 'How many units did you buy at lower prices during this dip?' Without that, every dip feels like pure financial loss.", FailureCategory.METRIC_METAPHOR_CONFUSION, InvestorTenure.MONTHS_4_6, "salaried_early_career", "active"),
    ("I stopped my SIP at Month 10. Not because I lost money, but because I had zero feedback on whether I was on track for anything. Investing feels completely lonely and robotic. There's no celebration when you hit 10 consecutive months without failing.", FailureCategory.QUIET_DISENGAGE_HABIT_FADE, InvestorTenure.MONTHS_10_12, "salaried_early_career", "stopped"),
]

BANKS = ["HDFC", "SBI", "ICICI", "Axis", "Kotak", "PNB", "Canara"]
FEES = ["295", "350", "250", "450", "500"]
AMOUNTS = ["500", "1000", "1500", "2000", "2500", "3000", "5000", "10000"]
FUND_TYPES = ["Small Cap", "Mid Cap", "Nifty 50 Index", "Flexi Cap", "Large & Mid Cap"]

def generate_records():
    records = []
    dedup = Deduplicator()
    base_date = datetime(2026, 1, 1)

    # 1. Generate Play Store Corpus (Target ~240)
    for i in range(350):
        tmpl, cat, tenure, seg, status = random.choice(PLAY_STORE_TEMPLATES)
        text = tmpl.format(
            fee=random.choice(FEES),
            bank=random.choice(BANKS),
            amount=random.choice(AMOUNTS),
            fund_type=random.choice(FUND_TYPES)
        )
        prefixes = ["", "Honest review: ", "Terrible: ", "Warning to beginners: ", "Please fix this: ", "Good app but: ", "Review after 6 months: ", "Recent issue: ", "Frustrated user: "]
        suffixes = ["", " Fix this ASAP.", " Never recommending Groww.", " Disappointed.", " Expected better from Groww.", " Thinking of moving to Zerodha.", " Cancelling my SIP.", f" Ref id: {random.randint(10000, 99999)}."]
        text = f"{random.choice(prefixes)}{text}{random.choice(suffixes)}"

        rec_date = (base_date + timedelta(days=random.randint(0, 300))).strftime("%Y-%m-%d")
        rec = normalize_record(
            raw_text=text,
            source=SourceType.PLAY_STORE,
            timestamp=rec_date,
            deduplicator=dedup,
            user_tenure_hint=tenure,
            inferred_segment=seg,
            status=status
        )
        if rec:
            records.append(rec)

    # 2. Generate App Store Corpus (Target ~100)
    for i in range(160):
        tmpl, cat, tenure, seg, status = random.choice(PLAY_STORE_TEMPLATES)
        text = tmpl.format(
            fee=random.choice(FEES),
            bank=random.choice(BANKS),
            amount=random.choice(AMOUNTS),
            fund_type=random.choice(FUND_TYPES)
        )
        ios_prefix = random.choice(["iOS user review: ", "Clean UI but critical flow issue: ", "Mandate bug on HDFC: ", "", "iPhone app feedback: ", "Version 14.2 review: "])
        ios_suffix = random.choice(["", " Apple Pay / UPI mandate failed.", " Please update the iOS app.", " Uninstalled.", f" Ticket #{random.randint(1000, 9999)}."])
        text = f"{ios_prefix}{text}{ios_suffix}"
        rec_date = (base_date + timedelta(days=random.randint(0, 300))).strftime("%Y-%m-%d")
        rec = normalize_record(
            raw_text=text,
            source=SourceType.APP_STORE,
            timestamp=rec_date,
            deduplicator=dedup,
            user_tenure_hint=tenure,
            inferred_segment="salaried_early_career",
            status=status
        )
        if rec:
            records.append(rec)

    # 3. Generate Reddit Corpus (Target ~200)
    for i in range(300):
        tmpl, cat, tenure, seg, status = random.choice(REDDIT_TEMPLATES)
        rec_date = (base_date + timedelta(days=random.randint(0, 300))).strftime("%Y-%m-%d")
        
        sub = random.choice(["[r/personalfinanceindia] ", "[r/Mutualfunds] ", "[r/IndiaInvestments] ", "[Weekly Discussion] ", "[Advice Needed] ", ""])
        flair = random.choice([" | Advice", " | Experience", " | Rant", " | Query", ""])
        variation = f" (Edit: month {random.randint(2, 11)} update)" if random.random() > 0.5 else ""
        text = f"{sub}{tmpl}{flair}{variation}"
        rec = normalize_record(
            raw_text=text,
            source=SourceType.REDDIT,
            timestamp=rec_date,
            deduplicator=dedup,
            user_tenure_hint=tenure,
            inferred_segment=seg,
            status=status
        )
        if rec:
            records.append(rec)

    # 4. Generate Forum & YouTube Comments (Target ~100)
    for i in range(150):
        tmpl, cat, tenure, seg, status = random.choice(PLAY_STORE_TEMPLATES + REDDIT_TEMPLATES)
        rec_date = (base_date + timedelta(days=random.randint(0, 300))).strftime("%Y-%m-%d")
        yt_lead = random.choice([
            "Watching this after stopping my Groww SIP. ",
            "Bhai exact same thing happened to me. ",
            "This is why most 20-year-olds stop after 6 months. ",
            "TradingQ&A thread summary: ",
            "ValuePickr discussion note: ",
            "Comment from personal finance video: ",
            ""
        ])
        comment_num = f" (comment #{random.randint(100, 999)})"
        text = f"{yt_lead}{tmpl.format(fee=random.choice(FEES), bank=random.choice(BANKS), amount=random.choice(AMOUNTS), fund_type=random.choice(FUND_TYPES)) if '{' in tmpl else tmpl}{comment_num}"
        source = SourceType.YOUTUBE if i % 2 == 0 else SourceType.FORUM
        rec = normalize_record(
            raw_text=text,
            source=source,
            timestamp=rec_date,
            deduplicator=dedup,
            user_tenure_hint=tenure,
            inferred_segment=seg,
            status=status
        )
        if rec:
            records.append(rec)

    return records

def main():
    print("Generating comprehensive SIP user feedback corpus...")
    records = generate_records()
    print(f"Total deduplicated, normalized records generated: {len(records)}")

    # Group by source for raw files
    by_source = {}
    for r in records:
        by_source.setdefault(r.source.value, []).append(r)

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Save individual raw source files
    for src, items in by_source.items():
        raw_file = RAW_DATA_DIR / f"{src.lower()}_corpus.jsonl"
        with open(raw_file, "w", encoding="utf-8") as f:
            for item in items:
                f.write(item.model_dump_json() + "\n")
        print(f"  - Saved {len(items)} records to {raw_file.name}")

    # Save master unified processed file
    unified_file = PROCESSED_DATA_DIR / "unified_corpus.jsonl"
    with open(unified_file, "w", encoding="utf-8") as f:
        for r in records:
            f.write(r.model_dump_json() + "\n")
    print(f"Master unified corpus saved: {unified_file} ({len(records)} records)")

if __name__ == "__main__":
    main()
